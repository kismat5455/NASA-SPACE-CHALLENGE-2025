# 🚀 NASA Research Assistant

A Retrieval-Augmented Generation (RAG) system for querying NASA research documents.

## 🌟 Features

- ☁️ **Cloud Storage**: All documents stored in Pinecone - accessible from any device
- 🔍 **Intelligent Document Search**: Query NASA research documents using natural language
- 🤖 **Powered by Google Gemini**: Uses Gemini 2.5 for advanced reasoning
- 📦 **LlamaIndex Framework**: Robust RAG implementation with cloud vector search
- 🌐 **Web Interface**: Beautiful Streamlit UI for interactive queries
- 📊 **Source Citations**: View relevant document excerpts with relevance scores
- 🖼️ **Multimodal Support**: Extract and analyze images from PDFs

## 🛠️ Technology Stack

- **LlamaIndex**: RAG framework for document indexing and retrieval
- **Google Gemini 2.5**: Advanced LLM for reasoning and generation
- **Pinecone**: Cloud vector database for scalable similarity search
- **Stella v5**: State-of-the-art local embeddings (1024 dimensions)
- **Streamlit**: Web interface for interactive queries
- **Python 3.13**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini access)
- Pinecone API Key (for cloud storage - free tier available)
- LLAMA_CLOUD_API_KEY(free tier available)

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

## 💡 Usage

Simply upload your PDF documents through the web interface and start asking questions. The system will search through your documents and provide relevant answers with source citations.

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

- **Model Selection**: Change models between Gemini 1.5 Flash or Pro
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




## 🤝 Contributing

This project is for NASA Space Challenge 2025. Feel free to extend and improve it!

## 📝 License

MIT License - Feel free to use and modify for your needs.

## 📚 Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Google Gemini API](https://ai.google.dev/)
- [NASA Open Data Portal](https://data.nasa.gov/)
- [Streamlit Documentation](https://docs.streamlit.io/)

