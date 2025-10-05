# 🚀 Quick Setup Guide - NASA RAG System

## Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get Your Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Click "Create API Key"
3. Copy the generated key

### Step 3: Create .env File

Create a file named `.env` in the project root with:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the key you copied.

### Step 4: Add NASA Documents

Create a `data` folder and add your NASA research documents:

```
data/
├── research_paper_1.pdf
├── technical_report.pdf
└── mission_document.txt
```

### Step 5: Index Your Documents

```bash
python document_ingestion.py
```

Wait for the indexing to complete. You'll see a success message.

### Step 6: Start Querying!

**Web Interface (Recommended):**
```bash
streamlit run app.py
```

**Command Line:**
```bash
python query_engine.py
```

## 🎯 Test Queries

Try these example queries:
- "What is the purpose of the Artemis program?"
- "Explain how the James Webb telescope works"
- "What are the challenges of Mars exploration?"

## ⚠️ Common Issues

**"No module named llama_index"**
- Run: `pip install -r requirements.txt`

**"API Key not found"**
- Make sure you created the `.env` file with your API key

**"No documents found"**
- Add PDF, TXT, DOCX, or MD files to the `data/` folder

## 📞 Need Help?

Check the main README.md for detailed documentation and troubleshooting.

---
Good luck with NASA Space Challenge 2025! 🚀

