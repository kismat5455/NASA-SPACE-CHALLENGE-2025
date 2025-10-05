"""
Document Ingestion Module for NASA RAG System
Handles loading and indexing NASA documents
"""
import os
import warnings
from typing import List

# Suppress Google gRPC warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
warnings.filterwarnings('ignore', category=DeprecationWarning)
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

try:
    from llama_parse import LlamaParse
    LLAMA_PARSE_AVAILABLE = True
except ImportError:
    LLAMA_PARSE_AVAILABLE = False
    print("⚠️  LlamaParse not installed. Install with: pip install llama-parse")

import config


class DocumentIngestion:
    """Handles document ingestion and indexing"""
    
    def __init__(self):
        """Initialize the document ingestion system"""
        # Set up LlamaIndex with Gemini
        Settings.llm = Gemini(
            model=config.GEMINI_MODEL,
            api_key=config.GOOGLE_API_KEY,
            temperature=0.7
        )
        
        # Use local embeddings if enabled, otherwise use Google embeddings
        if config.USE_LOCAL_EMBEDDINGS:
            print(f"🔧 Using local HuggingFace embeddings (no quota limits!)")
            print(f"📦 Model: {config.LOCAL_EMBEDDING_MODEL}")
            
            # Check if using Stella model and configure accordingly
            if "stella" in config.LOCAL_EMBEDDING_MODEL.lower():
                Settings.embed_model = HuggingFaceEmbedding(
                    model_name=config.LOCAL_EMBEDDING_MODEL,
                    trust_remote_code=True,
                    device="cpu",
                    config_kwargs={
                        "use_memory_efficient_attention": False,
                        "unpad_inputs": False
                    }
                )
            else:
                Settings.embed_model = HuggingFaceEmbedding(
                    model_name=config.LOCAL_EMBEDDING_MODEL,
                    trust_remote_code=True
                )
        else:
            print("🔧 Using Google Gemini embeddings")
            Settings.embed_model = GeminiEmbedding(
                model_name=config.EMBEDDING_MODEL,
                api_key=config.GOOGLE_API_KEY
            )
        
        Settings.chunk_size = config.CHUNK_SIZE
        Settings.chunk_overlap = config.CHUNK_OVERLAP
        
        self.index = None
    
    def load_documents(self, directory: str = None) -> List:
        """
        Load documents from directory
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of loaded documents
        """
        if directory is None:
            directory = config.DATA_DIR
        
        print(f"📚 Loading documents from {directory}...")
        
        # Check if directory exists and has files
        if not os.path.exists(directory):
            print(f"⚠️  Directory {directory} does not exist. Creating it...")
            os.makedirs(directory, exist_ok=True)
            return []
        
        files = os.listdir(directory)
        if not files:
            print(f"⚠️  No documents found in {directory}")
            return []
        
        # Check if we should use LlamaParse for PDFs
        if config.USE_LLAMA_PARSE and LLAMA_PARSE_AVAILABLE and config.LLAMA_CLOUD_API_KEY:
            print("🚀 Using LlamaParse for advanced PDF extraction (tables, images, etc.)")
            return self._load_with_llamaparse(directory)
        else:
            print("📄 Using standard PDF extraction (text only)")
            return self._load_with_simple_reader(directory)
    
    def _load_with_simple_reader(self, directory: str) -> List:
        """Load documents using SimpleDirectoryReader (basic parsing)"""
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True,
            required_exts=[".pdf", ".txt", ".docx", ".md"]
        )
        
        documents = reader.load_data()
        print(f"✅ Loaded {len(documents)} documents")
        return documents
    
    def _load_with_llamaparse(self, directory: str) -> List:
        """Load documents using LlamaParse (advanced PDF parsing)"""
        # Set up LlamaParse for PDFs
        parser = LlamaParse(
            api_key=config.LLAMA_CLOUD_API_KEY,
            result_type=config.LLAMA_PARSE_RESULT_TYPE,
            verbose=True,
            language="en"
        )
        
        # Use file extractor with LlamaParse for PDFs
        file_extractor = {".pdf": parser}
        
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True,
            required_exts=[".pdf", ".txt", ".docx", ".md"],
            file_extractor=file_extractor
        )
        
        documents = reader.load_data()
        print(f"✅ Loaded {len(documents)} documents with enhanced PDF parsing")
        return documents
    
    def create_index(self, documents: List = None, force_new: bool = False):
        """
        Create or load vector index
        
        Args:
            documents: List of documents to index
            force_new: Force creation of new index even if one exists
        """
        # Try to load existing index first
        if not force_new and os.path.exists(config.VECTOR_STORE_PATH):
            try:
                print(f"📂 Loading existing index from {config.VECTOR_STORE_PATH}...")
                storage_context = StorageContext.from_defaults(
                    persist_dir=config.VECTOR_STORE_PATH
                )
                self.index = load_index_from_storage(storage_context)
                print("✅ Index loaded successfully!")
                return self.index
            except Exception as e:
                print(f"⚠️  Could not load existing index: {e}")
                print("Creating new index...")
        
        # Create new index
        if documents is None:
            documents = self.load_documents()
        
        if not documents:
            print("❌ No documents to index. Please add documents to the data directory.")
            return None
        
        print("🔨 Creating vector index with Gemini embeddings...")
        self.index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True
        )
        
        # Persist index to disk
        print(f"💾 Saving index to {config.VECTOR_STORE_PATH}...")
        self.index.storage_context.persist(persist_dir=config.VECTOR_STORE_PATH)
        
        print("✅ Index created and saved successfully!")
        return self.index
    
    def get_index(self):
        """Get the current index"""
        if self.index is None:
            self.create_index()
        return self.index


def main():
    """Main function to run document ingestion"""
    print("=" * 60)
    print("NASA Document Ingestion System")
    print("=" * 60)
    
    # Check if API key is set
    if not config.GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in .env file")
        print("Please create a .env file with your Gemini API key")
        return
    
    # Initialize ingestion system
    ingestion = DocumentIngestion()
    
    # Load and index documents
    documents = ingestion.load_documents()
    
    if documents:
        ingestion.create_index(documents, force_new=True)
        print("\n✨ Document ingestion completed successfully!")
    else:
        print("\n⚠️  No documents found. Please add NASA documents to the 'data' directory.")
        print("Supported formats: PDF, TXT, DOCX, MD")


if __name__ == "__main__":
    main()

