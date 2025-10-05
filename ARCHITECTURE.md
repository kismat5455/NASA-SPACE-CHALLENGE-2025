# 🏗️ System Architecture - NASA RAG System

## Overview

This RAG (Retrieval-Augmented Generation) system combines document retrieval with AI generation to answer questions about NASA research documents.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌─────────────────┐              ┌────────────────────┐   │
│  │  Streamlit Web  │              │   CLI Interface    │   │
│  │   (app.py)      │              │ (query_engine.py)  │   │
│  └────────┬────────┘              └──────────┬─────────┘   │
└───────────┼───────────────────────────────────┼─────────────┘
            │                                   │
            └───────────────┬───────────────────┘
                           │
┌───────────────────────────▼──────────────────────────────────┐
│                     Query Engine                              │
│  • Question embedding (Gemini)                               │
│  • Vector similarity search                                  │
│  • Context retrieval                                         │
│  • Response generation (Gemini)                              │
└───────────────────────────┬──────────────────────────────────┘
                           │
┌───────────────────────────▼──────────────────────────────────┐
│                   Vector Store (ChromaDB)                     │
│  • Document embeddings                                       │
│  • Metadata storage                                          │
│  • Similarity search                                         │
└───────────────────────────┬──────────────────────────────────┘
                           │
┌───────────────────────────▼──────────────────────────────────┐
│                  Document Ingestion                          │
│  • Load documents (PDF, TXT, DOCX, MD)                      │
│  • Text extraction and chunking                             │
│  • Generate embeddings (Gemini)                             │
│  • Store in vector database                                 │
└───────────────────────────┬──────────────────────────────────┘
                           │
┌───────────────────────────▼──────────────────────────────────┐
│                    NASA Documents                            │
│                      (data/ folder)                          │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Document Ingestion (`document_ingestion.py`)

**Purpose:** Load and index NASA documents

**Process Flow:**
```
Documents → Load → Chunk → Embed → Store
```

**Key Functions:**
- `load_documents()`: Reads files from data directory
- `create_index()`: Creates vector embeddings and stores them
- Supports: PDF, TXT, DOCX, MD formats

**Technologies:**
- LlamaIndex's `SimpleDirectoryReader` for document loading
- Gemini Embedding API for creating vector representations
- ChromaDB for vector storage

### 2. Query Engine (`query_engine.py`)

**Purpose:** Process user queries and retrieve relevant information

**Process Flow:**
```
Query → Embed → Search → Retrieve Context → Generate Response
```

**Key Functions:**
- `query()`: Main query processing function
- `chat()`: Interactive CLI mode

**How It Works:**
1. User question is embedded using Gemini
2. Vector similarity search finds relevant document chunks
3. Top K most relevant chunks are retrieved
4. Chunks + question sent to Gemini for final answer
5. Response includes citations and source documents

### 3. Web Interface (`app.py`)

**Purpose:** User-friendly web interface for the RAG system

**Features:**
- Chat-based interface
- Real-time query processing
- Source citation display
- Session history management
- Configurable settings

**Technologies:**
- Streamlit for web framework
- Session state for chat history
- Caching for performance

### 4. Configuration (`config.py`)

**Purpose:** Central configuration management

**Settings:**
- API keys
- Model selection (Gemini 1.5 Flash/Pro)
- Chunk size and overlap
- Top K retrieval settings
- Directory paths

## Data Flow

### Indexing Phase
```
1. User places documents in data/
2. Run document_ingestion.py
3. Documents are loaded and chunked
4. Each chunk is embedded using Gemini
5. Embeddings stored in vector_store/
```

### Query Phase
```
1. User asks a question
2. Question is embedded
3. Vector search finds similar document chunks
4. Relevant chunks retrieved as context
5. Context + question sent to Gemini
6. Generated answer returned with sources
```

## Key Technologies

### LlamaIndex
- **Purpose:** RAG framework and orchestration
- **Features:**
  - Document loading and parsing
  - Text chunking strategies
  - Vector store integration
  - Query engine implementation

### Google Gemini
- **Models Used:**
  - `gemini-1.5-flash`: Fast responses, good for most queries
  - `gemini-1.5-pro`: Higher quality, complex reasoning
  - `embedding-001`: Text embeddings for vector search

### ChromaDB
- **Purpose:** Vector database for embeddings
- **Features:**
  - Efficient similarity search
  - Metadata filtering
  - Persistent storage

## RAG Process Explained

### What is RAG?

RAG (Retrieval-Augmented Generation) combines:
1. **Retrieval:** Finding relevant information from documents
2. **Generation:** Using AI to create natural language answers

### Why RAG?

- **Accuracy:** Grounds AI responses in actual documents
- **Citations:** Can point to specific sources
- **Updateable:** Add new documents without retraining
- **Domain-specific:** Focuses on your NASA documents

### How It Works

1. **Offline (Indexing):**
   - Break documents into chunks (1024 tokens)
   - Convert each chunk to a vector (embedding)
   - Store vectors in database

2. **Online (Querying):**
   - Convert user question to vector
   - Find most similar document chunks
   - Send question + chunks to AI
   - AI generates answer based on chunks

## Performance Considerations

### Chunk Size
- **Default:** 1024 tokens
- **Trade-off:** Larger = more context, smaller = more precise
- **Adjust in:** `config.py`

### Chunk Overlap
- **Default:** 200 tokens
- **Purpose:** Maintain context across boundaries
- **Prevents:** Information loss at chunk splits

### Top K Results
- **Default:** 5 documents
- **Trade-off:** More = comprehensive but slower
- **Adjust in:** `config.py` or web UI

### Model Selection
- **Flash:** Faster, cheaper, good for most queries
- **Pro:** Better reasoning, complex questions
- **Switch in:** `config.py`

## Extending the System

### Add New Document Types

Edit `document_ingestion.py`:
```python
reader = SimpleDirectoryReader(
    input_dir=directory,
    required_exts=[".pdf", ".txt", ".docx", ".md", ".csv"]  # Add .csv
)
```

### Use Different Vector Store

LlamaIndex supports:
- Pinecone
- Weaviate
- Qdrant
- FAISS

Change in document ingestion and query engine.

### Add Metadata Filtering

Filter by document type, date, etc:
```python
query_engine = index.as_query_engine(
    filters={"document_type": "research_paper"}
)
```

### Custom Prompts

Modify how Gemini responds:
```python
from llama_index.core import PromptTemplate

template = PromptTemplate(
    "You are a NASA research assistant. "
    "Answer based on: {context_str}\n"
    "Question: {query_str}\n"
    "Answer:"
)
```

## Security Considerations

### API Key Protection
- Never commit `.env` file
- Use environment variables
- Rotate keys regularly

### Document Access
- Store sensitive documents securely
- Consider access controls for production
- Encrypt data at rest if needed

### Rate Limiting
- Monitor API usage
- Implement rate limiting for public deployments
- Cache common queries

## Troubleshooting

### Slow Indexing
- Reduce chunk size
- Process documents in batches
- Use faster embedding model

### Poor Retrieval Quality
- Adjust chunk size and overlap
- Increase Top K results
- Improve document quality/formatting
- Try different embedding model

### Out of Memory
- Reduce chunk size
- Process fewer documents at once
- Use streaming for large files

### API Errors
- Check API key validity
- Monitor rate limits
- Verify network connectivity

## Future Enhancements

### Potential Features
- Multi-modal support (images, tables)
- Question refinement and suggestions
- Answer validation and fact-checking
- User feedback integration
- Advanced analytics dashboard
- Batch query processing
- API endpoint for integration

### Scalability
- Cloud deployment (AWS, GCP, Azure)
- Distributed vector store
- Caching layer (Redis)
- Load balancing
- Monitoring and logging

## Resources

- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [RAG Explained](https://arxiv.org/abs/2005.11401)
- [Vector Databases Guide](https://www.pinecone.io/learn/vector-database/)

---

Built for NASA Space Challenge 2025 🚀

