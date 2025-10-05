"""
Configuration file for NASA RAG System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")  # For LlamaParse

# Model Configuration
GEMINI_MODEL = "gemini-2.0-flash"  # Using Gemini 2.0 Flash
EMBEDDING_MODEL = "models/embedding-001"  # Google embedding (has quota limits)
USE_LOCAL_EMBEDDINGS = True  # Set to True to use free local HuggingFace embeddings
LOCAL_EMBEDDING_MODEL = "dunzhang/stella_en_400M_v5"  # Stella v5: SOTA embeddings (Jan 2025)

# Storage Configuration
VECTOR_STORE_PATH = "./vector_store"
DATA_DIR = "./data"

# RAG Configuration
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5

# PDF Parsing Configuration
USE_LLAMA_PARSE = True  # Use LlamaParse for better PDF extraction (tables, images, etc.)
LLAMA_PARSE_RESULT_TYPE = "markdown"  # or "text"

# Create directories if they don't exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

