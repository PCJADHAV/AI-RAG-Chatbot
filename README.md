# 🤖 AI RAG Chatbot (Real-Time Assistant)

An intelligent **AI-powered chatbot** that answers user queries using **Retrieval-Augmented Generation (RAG)** with vector search.

Built with **Streamlit, Pinecone, Sentence Transformers, and Groq LLM**.

---

## 🚀 Features

* 💬 Interactive chatbot UI (Streamlit)
* 🔍 Semantic search using embeddings
* 🧠 Context-aware AI responses
* ⚡ Fast retrieval using Pinecone vector DB
* 🗂 Multi-chat session support
* 🎨 Clean and responsive UI

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **LLM:** Groq (GPT-OSS-20B)
* **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
* **Vector Database:** Pinecone
* **Language:** Python

---

## ⚙️ Setup Instructions

### 1. Clone Repository
git clone (https://github.com/PCJADHAV/AI-RAG-Chatbot.git)
cd ai-rag-chatbot

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Create .env File
groq_api_key=your_groq_api_key, 
pinecone_api_key=your_pinecone_api_key

### 4. Run the App
streamlit run app/main.py

---

## ⚙️ How It Works

1. User enters a query in chatbot
2. Query is converted into vector embeddings
3. Pinecone retrieves most relevant context
4. Context + query sent to LLM
5. AI generates accurate, context-based response

---

## 🎯 Use Cases

* AI-powered knowledge assistant
* Document-based chatbot
* Customer support automation
* Research assistant

---

## 🚀 Future Improvements

* Upload documents via UI
* Chat history persistence
* Multi-language support
* Cloud deployment (AWS / Render / Streamlit Cloud)
