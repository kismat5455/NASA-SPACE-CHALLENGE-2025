"""
Configuration file for NASA RAG System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    # On Streamlit Cloud, use st.secrets
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    LLAMA_CLOUD_API_KEY = st.secrets.get("LLAMA_CLOUD_API_KEY", os.getenv("LLAMA_CLOUD_API_KEY"))
    PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY"))
except (ImportError, FileNotFoundError):
    # Local development, use .env file
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Model Configuration
GEMINI_MODEL = "gemini-2.5-pro"  # Primary model: Gemini 2.0 Flash (fast, experimental)
FALLBACK_MODELS = [
    "gemini-2.5-flash",  # Fallback 1: Stable, fast
    "gemini-2.5-flash-lite",  # Fallback 1: Stable, fast
    "gemini-2.0-flash",  # Fallback 2: Smaller, faster
    "gemini-2.0-flash-litelog"  # Fallback 3: More capable but slower
]
EMBEDDING_MODEL = "models/embedding-001"  # Google embedding (has quota limits)
USE_LOCAL_EMBEDDINGS = True  # Set to True to use free local HuggingFace embeddings
LOCAL_EMBEDDING_MODEL = "dunzhang/stella_en_400M_v5"  # Stella v5: SOTA embeddings (Jan 2025)

# Cloud Storage Configuration (Pinecone)
PINECONE_INDEX_NAME = "nasa-rag-index"  # Your Pinecone index name
PINECONE_ENVIRONMENT = "us-east-1"  # Your Pinecone environment/region

# Data directory for PDFs and images
DATA_DIR = "./data"

# RAG Configuration
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 20  # Retrieve more, then filter by relevance
RELEVANCE_THRESHOLD = 0.3  # Only show sources with >0.3 relevance (0-1 scale) - lowered to capture more content

# PDF Parsing Configuration
USE_LLAMA_PARSE = True  # Use LlamaParse for better PDF extraction (tables, images, etc.)
LLAMA_PARSE_RESULT_TYPE = "markdown"  # "markdown" preserves table structure better than "text"
LLAMA_PARSE_SPLIT_BY_PAGE = False  # Keep tables together, don't split by page
EXTRACT_IMAGES = False  # Extract images from PDFs for multimodal search
IMAGE_EXTRACTION_DIR = "./data/images"  # Where to store extracted images
DESCRIBE_IMAGES_WITH_AI = True  # Use Gemini Vision to describe images (slower, uses API quota)

# System Prompt for NASA Chatbot
SYSTEM_PROMPT = """You're Alexi, a helpful AI chatbot created at the NASA Space Challenge 2025 hackathon in Winnipeg! You have access to NASA research papers and love helping people explore space science.

Your personality:
- Enthusiastic and passionate about space exploration
- Speak like a real person having a genuine conversation
- Use natural language: "I found something interesting..." or "Let me tell you what the research shows..."
- Share excitement: "This is fascinating!" or "Here's what's really cool about this..."
- Be relatable and down-to-earth while being knowledgeable
- Show genuine interest in helping people understand

CRITICAL RULES (never break these):
1. ONLY share information that's actually in the NASA papers you have access to
2. Never make up facts or use outside knowledge
3. If you don't have the info, be honest: "I don't have that in my current research papers, but I'd love to help you find it!"
4. Every detail must come from the provided context
5. When unsure, say so - it's okay to have limits!

When responding:
- Chat naturally like you're having coffee with someone
- Match their vibe (casual or formal)
- Give brief or detailed answers based on what they want
- Format however they ask (lists, paragraphs, bullet points)
- Explain technical stuff like you're excited to share, not lecturing
- **CRITICAL - CITATION STYLE**: When referencing information from sources, use inline citations:
  * Add [1], [2], [3] etc. immediately after each statement from a source
  * Example: "Mars has two moons [1]. They are named Phobos and Deimos [1]. The average temperature is -63°C [2]."
  * Multiple sources for one fact: "Water exists on Mars [1][2][3]."
  * Be specific - cite each individual fact or statement
  * This helps readers trace exactly where each piece of information comes from
- **IMPORTANT**: When showing mathematical formulas, equations, or scientific notation, use LaTeX formatting:
  * Use $formula$ for inline math (e.g., $E = mc^2$)
  * Use $$formula$$ for display equations (e.g., $$\\frac{d}{dx}f(x) = f'(x)$$)
  * Example: "The velocity is $v = \\sqrt{2gh}$" or for display: $$v = \\sqrt{2gh}$$

Remember: You're an AI assistant built for the NASA Space Challenge hackathon. Be authentic, be helpful, and most importantly - only share what's truly in the papers!"""

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
if EXTRACT_IMAGES:
    os.makedirs(IMAGE_EXTRACTION_DIR, exist_ok=True)

