# 🚀 NASA Research Assistant - RAG System

A Retrieval-Augmented Generation (RAG) system for querying NASA research documents, built for NASA Space Challenge 2025.

## 🌟 Features

- **Intelligent Document Search**: Query NASA research documents using natural language
- **Powered by Google Gemini**: Uses Gemini 1.5 for both embeddings and generation
- **LlamaIndex Framework**: Robust RAG implementation with vector search
- **Multiple Interfaces**: 
  - Command-line interface
  - Interactive web UI (Streamlit)
- **Source Citations**: View relevant document excerpts with relevance scores
- **Easy Document Management**: Simply drop documents into the data folder

## 🛠️ Technology Stack

- **LlamaIndex**: RAG framework for document indexing and retrieval
- **Google Gemini**: LLM for embeddings and text generation
- **ChromaDB**: Vector database for efficient similarity search
- **Streamlit**: Web interface for interactive queries
- **Python 3.8+**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini access)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd NASA-SPACE-CHALLENGE-2025

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get your Google API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API key
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Add NASA Documents

Place your NASA research documents in the `data/` folder:

```
data/
├── research_paper_1.pdf
├── technical_report.pdf
├── mission_overview.txt
└── ...
```

Supported formats: PDF, TXT, DOCX, MD

### 4. Index Documents

Run the document ingestion script to create the vector index:

```bash
python document_ingestion.py
```

This will:
- Load all documents from the `data/` folder
- Create embeddings using Gemini
- Store the vector index in `vector_store/`

### 5. Query Documents

**Option A: Web Interface (Recommended)**

```bash
streamlit run app.py
```

Then open your browser to http://localhost:8501

**Option B: Command Line Interface**

```bash
python query_engine.py
```

## 💡 Usage Examples

### Example Queries

- "What are the main objectives of the Artemis mission?"
- "Explain the James Webb Space Telescope's infrared capabilities"
- "What are the challenges of Mars colonization?"
- "Summarize NASA's climate research initiatives"
- "How does the ISS maintain its orbit?"

## 🏗️ Project Structure

```
NASA-SPACE-CHALLENGE-2025/
├── config.py                 # Configuration settings
├── document_ingestion.py     # Document loading and indexing
├── query_engine.py           # Query interface (CLI)
├── app.py                    # Streamlit web interface
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this)
├── .env.example             # API key template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── data/                    # Place your documents here
└── vector_store/            # Vector index storage (auto-created)
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Model Selection**: Change between Gemini 1.5 Flash or Pro
- **Chunk Size**: Adjust document chunking parameters
- **Top K Results**: Number of relevant documents to retrieve
- **Storage Paths**: Modify data and index directories

```python
# Example configuration changes
GEMINI_MODEL = "models/gemini-1.5-pro"  # Use Pro for better quality
CHUNK_SIZE = 2048                        # Larger chunks
TOP_K_RESULTS = 10                       # More sources
```

## 🔧 Advanced Features

### Re-indexing Documents

To rebuild the index after adding new documents:

```bash
python document_ingestion.py
```

The system will detect and re-index all documents.

### Customizing Responses

Modify the temperature and response settings in `config.py` or directly in the code:

```python
Settings.llm = Gemini(
    model=config.GEMINI_MODEL,
    api_key=config.GOOGLE_API_KEY,
    temperature=0.7  # Lower for more focused, higher for creative
)
```

## 🐛 Troubleshooting

### "No module named 'llama_index'"

```bash
pip install -r requirements.txt
```

### "API Key not found"

Make sure you've created a `.env` file with your Google API key.

### "No documents found"

Place PDF, TXT, DOCX, or MD files in the `data/` folder and run `document_ingestion.py`.

### Import Errors

If you see version conflicts, try:

```bash
pip install --upgrade llama-index google-generativeai
```

## 📊 Performance Tips

1. **Use Gemini 1.5 Pro** for complex research questions
2. **Use Gemini 1.5 Flash** for faster responses on simpler queries
3. **Adjust chunk size** based on your document types
4. **Increase TOP_K_RESULTS** for more comprehensive answers
5. **Pre-process PDFs** to ensure clean text extraction

## 🤝 Contributing

This project is for NASA Space Challenge 2025. Feel free to extend and improve it!

## 📝 License

MIT License - Feel free to use and modify for your needs.

## 🎯 NASA Space Challenge 2025

This RAG system is designed to help researchers, scientists, and space enthusiasts access and understand NASA's vast repository of research documents efficiently.

**Good luck with your NASA Space Challenge! 🚀🌙**

## 📚 Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Google Gemini API](https://ai.google.dev/)
- [NASA Open Data Portal](https://data.nasa.gov/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the LlamaIndex and Gemini documentation
3. Check your API key and quota limits

---

Built with ❤️ for NASA Space Challenge 2025

