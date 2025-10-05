# ⚡ Quick Start - Get Running in 5 Minutes

## 🎯 Prerequisites
- Python 3.8 or higher
- Google Gemini API key

## 🚀 Setup Steps

### 1️⃣ Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure API Key (1 minute)

1. Get your API key: https://makersuite.google.com/app/apikey
2. Create `.env` file in project root:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3️⃣ Add Documents (30 seconds)

Place your NASA documents in the `data/` folder:
- Supported: PDF, TXT, DOCX, MD
- A sample document is already included!

### 4️⃣ Index Documents (1-2 minutes)

```bash
python document_ingestion.py
```

### 5️⃣ Start Querying! (30 seconds)

**Web UI (Recommended):**
```bash
streamlit run app.py
```

**Command Line:**
```bash
python query_engine.py
```

## ✅ Verify Setup

Run the quick check script:
```bash
python quickstart.py
```

## 🎯 Try These Queries

- "What is the Artemis program?"
- "When is Artemis III scheduled to launch?"
- "What is the purpose of the Lunar Gateway?"

## 🆘 Issues?

**"No module named llama_index"**
→ Run: `pip install -r requirements.txt`

**"API Key not found"**
→ Create `.env` file with your API key

**Need more help?**
→ See `README.md` or `setup_guide.md`

---

**You're ready! Good luck with NASA Space Challenge 2025! 🚀**

