# 🚀 TrendScope AI

**TrendScope AI** is an AI-powered trend intelligence platform that crawls the web, analyzes emerging topics, measures their velocity, and generates human-readable insights using local LLMs.

The platform is designed for **real-time awareness**, **data-driven decision-making**, and **modern dashboard visualization**.

---

## ✨ Features

### ✅ Implemented
- 🔎 **Web ingestion** (Google News RSS)
- 🧹 **Text cleaning & normalization**
- 🏷 **Topic classification** (AI, politics, technology, etc.)
- 📊 **Topic velocity & hotness scoring**
- 🤖 **AI-generated topic insights** (cached in DB)
- 🗂 **PostgreSQL-backed analytics**
- 📡 **REST API (FastAPI)**
- 🖥 **Dashboard v2 (React + TypeScript)**

### 🚧 In Progress
- Time-series velocity charts
- Advanced UI animations & transitions
- Additional data sources (YouTube, social platforms)
- Subscription / notification system

---

## 🧠 Architecture Overview

Web Sources
↓
Extractors (RSS / Crawlers)
↓
Raw Events
↓
Text Cleaner + Topic Classifier
↓
Clean Events (PostgreSQL)
↓
Analytics (Velocity, Hotness)
↓
AI Insight Generator (Local LLM)
↓
FastAPI → React Dashboard


---

## 🛠 Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **LangDetect**
- **Local LLM (Ollama / llama3.1)**

### Frontend
- **React**
- **TypeScript**
- **Vite**
- **Tailwind CSS**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/trendscope-ai.git
cd trendscope-ai
2️⃣ Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


Configure your database in .env:

DATABASE_URL=postgresql://user:password@localhost:5432/trendscope


Run migrations / create tables:

python -m app.db.init_db


Load initial data:

python -m scripts.load_google_news


Start the API:

uvicorn main:app --reload


API will be available at:

http://127.0.0.1:8000


Swagger docs:

http://127.0.0.1:8000/docs

3️⃣ Frontend setup
cd frontend
npm install
npm run dev


Dashboard runs on:

http://localhost:5173

🔌 Key API Endpoints
Endpoint	Description
/api/trends/velocity	Topic velocity & hotness
/api/trends/keywords	Trending keywords
/api/trends/sources	Source distribution
/api/topics/{topic}	Topic details + AI insight
/api/health	Health check
📌 Project Status

Backend: Stable

Data pipeline: Operational

AI insights: Cached & reliable

Frontend: v2 in progress

Deployment: Local / GitHub (current)

🙌 Acknowledgements

Built with curiosity, persistence, and a lot of debugging.

TrendScope AI is an evolving project — feedback and contributions are welcome.