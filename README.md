---
title: Resume Shortlister AI
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# 🤖 Resume Shortlister AI

An intelligent resume shortlisting system built with RAG (Retrieval Augmented Generation) 
that helps HR teams filter and rank candidates based on job requirements.

## 🎯 Problem It Solves

HR teams manually read hundreds of resumes for every job opening — slow, biased, and inefficient.
This system automates candidate shortlisting using AI — finding the best matches in seconds.

## ✨ Features

- 📄 Upload multiple resumes in PDF format
- 🔍 Semantic search — finds candidates by meaning, not just keywords
- 🤖 LLM-powered analysis — explains WHY each candidate matches
- 📊 Match scoring — ranks candidates from best to worst fit
- 🗑️ Delete candidates from database
- 💾 Persistent storage — data survives restarts

## 🏗️ System Architecture
PDF Resume → Text Extraction → Chunking → Embeddings → Vector DB
↑
HR Query → Embed Query → Semantic Search → Top Chunks ──────┘
↓
LLM Analysis
↓
Ranked Candidates + Explanation

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Embeddings |HuggingFace `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| LLM | Groq (Llama 3.3 70B) |
| PDF Extraction | PyMuPDF |
| Text Splitting | LangChain |
| Language | Python 3.10+ |

## 📁 Project Structure
resume-shortlister/
│
├── app.py          → Streamlit UI
├── ingestion.py    → PDF text extraction
├── embeddings.py   → Text chunking + vectorization
├── retrieval.py    → ChromaDB storage + semantic search
├── ranker.py       → LLM ranking + explanation
├── uploads/        → Resume PDFs (gitignored)
├── data/           → ChromaDB files (gitignored)
└── requirements.txt


## 🚀 How To Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Shronly/resume-shortlister.git
cd resume-shortlister
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up API keys**
Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_her

Get your free Groq API key at: https://console.groq.com

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 💡 How It Works

**Step 1 — Resume Ingestion:**
PDF resumes are uploaded and text is extracted using PyMuPDF.
Text is split into overlapping chunks of 500 characters.

**Step 2 — Embedding:**
Each chunk is converted into a 384-dimensional vector using
the `all-MiniLM-L6-v2` sentence transformer model.
These vectors capture the semantic meaning of the text.

**Step 3 — Storage:**
Vectors are stored in ChromaDB — a vector database optimized
for similarity search. Data persists on disk permanently.

**Step 4 — Semantic Search:**
When HR enters a job requirement, it is embedded using the
same model. ChromaDB finds resume chunks whose vectors are
closest to the query vector using cosine similarity.

**Step 5 — LLM Ranking:**
Top matching chunks are sent to Groq's Llama 3.3 70B model
with a structured prompt. The LLM analyzes each candidate
and provides matching skills, missing skills, and a final
recommendation.

## 🎓 Key Concepts Learned

- RAG (Retrieval Augmented Generation) pipeline
- Vector embeddings and semantic search
- ChromaDB vector database
- Prompt engineering for structured LLM output
- Streamlit for AI application UI
- API integration (Groq)

## 👨‍💻 Author

**Shreyash Aryaa**
- GitHub: [@Shronly](https://github.com/Shronly)
- Email: shreyashshr08@gmail.com