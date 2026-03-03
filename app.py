import os
import streamlit as st
import google.generativeai as genai

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------- UI Setup ----------------
st.set_page_config(page_title="Nova PDF AI Chatbot", layout="centered")
st.title("📄 Nova PDF AI Chatbot")


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")

    api_key = st.text_input("Enter Gemini API Key:", type="password")

    if st.button("Clear Chat History"):
        st.session_state.vector_db = None
        st.session_state.chat_history = []
        st.success("Chat history cleared!")


# ---------------- Initialize Memory ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- Core Logic ----------------
if api_key:
    try:
        genai.configure(api_key=api_key)

        # ========= MULTI-PDF UPLOAD =========
        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_files:

            # Process only once
            if "vector_db" not in st.session_state:

                with st.spinner("Indexing PDFs..."):

                    all_docs = []

                    for file in uploaded_files:
                        temp_path = f"temp_{file.name}"

                        with open(temp_path, "wb") as f:
                            f.write(file.read())

                        loader = PyPDFLoader(temp_path)
                        documents = loader.load()
                        all_docs.extend(documents)

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )

                    docs = splitter.split_documents(all_docs)

                    embeddings = HuggingFaceEmbeddings(
                        model_name="all-MiniLM-L6-v2"
                    )

                    st.session_state.vector_db = FAISS.from_documents(
                        docs, embeddings
                    )

                    st.success("PDFs indexed successfully!")


            # ========= SUMMARY BUTTON =========
            if st.button("📑 Summarize Documents"):

                summary_docs = st.session_state.vector_db.similarity_search(
                    "Summarize the document",
                    k=5
                )

                summary_context = "\n".join(
                    [doc.page_content for doc in summary_docs]
                )

                model = genai.GenerativeModel("gemini-2.5-flash")

                summary = model.generate_content(
                    f"Provide a concise summary of this document:\n{summary_context}"
                )

                st.subheader("📑 Summary")
                st.info(summary.text)


            # ========= CHAT INTERFACE =========
            question = st.chat_input("Ask something about the document...")

            if question and "vector_db" in st.session_state:

                relevant_docs = st.session_state.vector_db.similarity_search(
                    question,
                    k=3
                )

                context = "\n".join(
                    [doc.page_content for doc in relevant_docs]
                )

                model = genai.GenerativeModel("gemini-2.5-flash")

                prompt = f"""
                Context:
                {context}

                Question: {question}

                Answer ONLY using the context above.
                """

                with st.spinner("Nova is thinking..."):
                    response = model.generate_content(prompt)

                    answer = response.text

                    # Save to history
                    st.session_state.chat_history.append(
                        {"q": question, "a": answer}
                    )


            # ========= DISPLAY CHAT HISTORY =========
            for chat in reversed(st.session_state.chat_history):
                st.markdown(f"**🧑 You:** {chat['q']}")
                st.markdown(f"**🤖 Nova:** {chat['a']}")
                st.divider()


            # ========= SHOW SOURCES =========
            if question and "vector_db" in st.session_state:

                st.subheader("📄 Sources")

                for doc in relevant_docs:
                    page = doc.metadata.get("page", "Unknown")
                    st.write(f"Page: {page}")


    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

else:
    st.warning("Please enter your API Key in the sidebar.")