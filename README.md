# 📄 Nova PDF AI Chatbot

An AI-powered chatbot that allows users to upload one or multiple PDF documents and ask questions in natural language.  
The system uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-based answers from the uploaded files.

---

## 🚀 Features

- 📂 Upload single or multiple PDFs  
- 🤖 Ask questions about document content  
- 🔍 Semantic search using embeddings  
- ⚡ Fast vector retrieval with FAISS  
- 🧠 Gemini LLM for answer generation  
- 💻 Interactive Streamlit interface  
- 🔒 Secure API key input via sidebar  
- 🧹 Clear chat / reset database option  

---

## 🧠 How It Works (RAG Pipeline)

```
PDF Upload 
   ↓
Text Extraction 
   ↓
Chunking 
   ↓
Embeddings Generation 
   ↓
Vector Storage (FAISS) 
   ↓
Relevant Chunk Retrieval 
   ↓
Gemini LLM Processing 
   ↓
Final Answer Generation
```

---

## 🛠️ Tech Stack

| Component | Technology Used |
|-----------|-----------------|
| Frontend  | Streamlit |
| LLM | Google Gemini (gemini-2.5-flash) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| Document Processing | LangChain |
| Backend Language | Python |

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/nova-pdf-ai-chatbot.git
cd nova-pdf-ai-chatbot
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python -m streamlit run app.py
```

---

## 🔑 API Configuration

- Enter your **Google Gemini API Key** in the sidebar.
- The app will initialize the LLM and start processing PDFs.

---

## 📂 Project Structure

```
nova-pdf-ai-chatbot/
│── app.py
│── requirements.txt
│── README.md
│── utils/
│── vector_store/
```

---

## 🌟 Future Improvements

- Chat history memory  
- Cloud deployment (Streamlit Cloud / AWS)  
- Multi-format support (DOCX, TXT)  
- User authentication  

---

## 👩‍💻 Author

**Nishita Rajak**  
AI/ML & Generative AI Enthusiast  
