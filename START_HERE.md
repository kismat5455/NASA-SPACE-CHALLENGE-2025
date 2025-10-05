# 🚀 START HERE - NASA RAG System

## ✅ What's Been Created

Your complete RAG system for NASA documents is ready! Here's what you have:

```
NASA-SPACE-CHALLENGE-2025/
│
├── 📄 START_HERE.md          ← YOU ARE HERE
├── ⚡ QUICKSTART.md           ← Read this first! (5 min setup)
├── 📘 README.md              ← Full documentation
├── 🏗️ ARCHITECTURE.md         ← Technical deep-dive
├── 📋 PROJECT_SUMMARY.md     ← Overview of everything
├── 📖 setup_guide.md         ← Step-by-step instructions
│
├── 🐍 Python Files
│   ├── config.py             ← Settings and configuration
│   ├── document_ingestion.py ← Index NASA documents
│   ├── query_engine.py       ← Query documents (CLI)
│   ├── app.py                ← Web interface (Streamlit)
│   └── quickstart.py         ← Verify setup
│
├── 🪟 Windows Helpers
│   ├── install.bat           ← Easy installation
│   ├── run_web.bat           ← Launch web interface
│   └── run_cli.bat           ← Launch CLI
│
├── ⚙️ Configuration
│   ├── requirements.txt      ← Python dependencies
│   ├── env_template.txt      ← API key template
│   └── .env                  ← CREATE THIS with your API key
│
└── 📁 Directories
    ├── data/                 ← Add NASA documents here
    │   └── sample_nasa_document.txt (included!)
    └── vector_store/         ← Auto-created for embeddings
```

## 🎯 Get Started in 3 Minutes

### Option 1: Windows Quick Install (EASIEST)

1. **Double-click** `install.bat`
2. **Create** `.env` file with your API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```
   Get key from: https://makersuite.google.com/app/apikey

3. **Double-click** `run_web.bat`

Done! 🎉

### Option 2: Manual Setup (All Platforms)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your API key
# (Copy env_template.txt to .env and edit)

# 3. Index documents
python document_ingestion.py

# 4. Launch interface
streamlit run app.py
```

## 🧪 Test It Out

The system includes a sample NASA document about Artemis. Try these queries:

1. "What is the Artemis program?"
2. "When is Artemis III scheduled?"
3. "What is the Lunar Gateway?"

## 📚 What to Read Next

Choose based on your needs:

| If you want to... | Read this... |
|------------------|--------------|
| **Get started ASAP** | `QUICKSTART.md` |
| **Understand everything** | `README.md` |
| **Step-by-step guide** | `setup_guide.md` |
| **Know how it works** | `ARCHITECTURE.md` |
| **See what you have** | `PROJECT_SUMMARY.md` |

## 🎓 Key Concepts

### What is RAG?
**Retrieval-Augmented Generation** = Smart document search + AI generation

1. Your documents → Converted to searchable vectors
2. Your question → Converted to a vector
3. System finds → Most relevant document chunks
4. AI generates → Answer based on those chunks
5. You get → Answer + sources

### Why It's Cool
- ✅ Answers are based on YOUR documents
- ✅ Provides source citations
- ✅ No retraining needed
- ✅ Update by adding documents

## 🔑 Important: API Key Required

You need a **free** Google Gemini API key:

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Create `.env` file:
   ```
   GOOGLE_API_KEY=paste_your_key_here
   ```

## 💡 Tips

### Adding Documents
- Drop any PDF, TXT, DOCX, or MD files into `data/`
- Run `python document_ingestion.py` to index them
- That's it!

### Best Results
- Use well-formatted documents
- Ask specific questions
- Try different phrasings
- Check the sources provided

### Customize
- Edit `config.py` to change settings
- Switch between Gemini Flash (fast) and Pro (better)
- Adjust chunk sizes and retrieval numbers

## 🛠️ Verify Setup

Run the diagnostic tool:

```bash
python quickstart.py
```

This checks:
- ✅ Python version
- ✅ Dependencies installed
- ✅ API key configured
- ✅ Documents available
- ✅ Index created

## 🌟 Two Ways to Use

### 1. Web Interface (Recommended)
```bash
streamlit run app.py
```
- Beautiful chat interface
- Shows sources inline
- Session history
- Easy to use

### 2. Command Line
```bash
python query_engine.py
```
- Fast and lightweight
- Perfect for testing
- Great for automation

## 🏆 For NASA Space Challenge 2025

This system helps you:
- 📖 Research NASA missions quickly
- 🔍 Find specific information in documents
- 📝 Get cited, accurate answers
- 🚀 Build on top with your own features

## 🆘 Having Issues?

### Quick Fixes

**Error: No module named 'llama_index'**
```bash
pip install -r requirements.txt
```

**Error: API key not found**
- Make sure `.env` file exists
- Check the API key is correct
- No spaces or quotes needed

**Error: No documents found**
- Add files to `data/` folder
- Run `python document_ingestion.py`

**Still stuck?**
- Check `README.md` troubleshooting section
- Run `python quickstart.py` for diagnostics

## 📞 Resources

- 📘 [LlamaIndex Docs](https://docs.llamaindex.ai/)
- 🤖 [Gemini API](https://ai.google.dev/)
- 🌐 [Streamlit Docs](https://docs.streamlit.io/)
- 🔬 [NASA Data](https://data.nasa.gov/)

## 🎉 You're All Set!

**Next steps:**
1. ✅ Read `QUICKSTART.md`
2. ✅ Get your API key
3. ✅ Run `install.bat` or `pip install -r requirements.txt`
4. ✅ Create `.env` with your key
5. ✅ Run `python document_ingestion.py`
6. ✅ Launch with `streamlit run app.py`
7. ✅ Start querying!

---

## 🌙 Good Luck with NASA Space Challenge 2025! 🚀

*"That's one small step for code, one giant leap for your project"*

---

**Built with:**
- 🧠 Google Gemini AI
- 📚 LlamaIndex
- 🔍 Vector Search
- 🐍 Python
- ❤️ Passion for space exploration

**Questions?** Check the docs or run `python quickstart.py`

