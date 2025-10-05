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
    Settings
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Cloud storage imports
try:
    from pinecone import Pinecone, ServerlessSpec
    from llama_index.vector_stores.pinecone import PineconeVectorStore
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("⚠️  Pinecone not installed. Install with: pip install pinecone-client llama-index-vector-stores-pinecone")

try:
    from llama_parse import LlamaParse
    LLAMA_PARSE_AVAILABLE = True
except ImportError:
    LLAMA_PARSE_AVAILABLE = False
    print("⚠️  LlamaParse not installed. Install with: pip install llama-parse")

try:
    from multimodal_processor import process_pdf_multimodal
    MULTIMODAL_AVAILABLE = True
except ImportError:
    MULTIMODAL_AVAILABLE = False
    print("⚠️  Multimodal processor not available")

import config


class DocumentIngestion:
    """Handles document ingestion and indexing"""
    
    def __init__(self):
        """Initialize the document ingestion system"""
        # Set up AI model
        Settings.llm = Gemini(
            model=config.GEMINI_MODEL,
            api_key=config.GOOGLE_API_KEY,
            temperature=0.7
        )
        
        # Set up embeddings (local or Google)
        self._setup_embeddings()
        
        Settings.chunk_size = config.CHUNK_SIZE
        Settings.chunk_overlap = config.CHUNK_OVERLAP
        
        self.index = None
        self.vector_store = None
        
        # Initialize cloud storage
        self._init_cloud_storage()
    
    def _setup_embeddings(self):
        """Set up embeddings (local or Google)"""
        if config.USE_LOCAL_EMBEDDINGS:
            # Stella model needs special config
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
            Settings.embed_model = GeminiEmbedding(
                model_name=config.EMBEDDING_MODEL,
                api_key=config.GOOGLE_API_KEY
            )
    
    def _init_cloud_storage(self):
        """Initialize Pinecone cloud vector storage"""
        if not PINECONE_AVAILABLE:
            print("❌ Pinecone not available. Install with: pip install pinecone-client llama-index-vector-stores-pinecone")
            raise ImportError("Pinecone is required")
        
        if not config.PINECONE_API_KEY:
            print("❌ PINECONE_API_KEY not found in .env file")
            raise ValueError("PINECONE_API_KEY is required in .env file")
        
        try:
            pc = Pinecone(api_key=config.PINECONE_API_KEY)
            existing_indexes = [idx.name for idx in pc.list_indexes()]
            
            # Get embedding dimension
            embed_dim = self._get_embedding_dimension()
            
            # Create or recreate index if needed
            if config.PINECONE_INDEX_NAME not in existing_indexes:
                self._create_pinecone_index(pc, embed_dim)
            else:
                self._verify_index_dimensions(pc, embed_dim)
            
            # Connect to the index
            pinecone_index = pc.Index(config.PINECONE_INDEX_NAME)
            self.vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
            
        except Exception as e:
            print(f"❌ Error initializing Pinecone: {e}")
            raise
    
    def _get_embedding_dimension(self):
        """Get the embedding dimension from the model"""
        if hasattr(Settings.embed_model, 'embed_dim'):
            return Settings.embed_model.embed_dim
        
        # Try to get dimension by creating a test embedding
        try:
            test_embedding = Settings.embed_model.get_text_embedding("test")
            return len(test_embedding)
        except:
            return 768  # Default fallback
    
    def _create_pinecone_index(self, pc, embed_dim):
        """Create a new Pinecone index"""
        pc.create_index(
            name=config.PINECONE_INDEX_NAME,
            dimension=embed_dim,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=config.PINECONE_ENVIRONMENT
            )
        )
    
    def _verify_index_dimensions(self, pc, embed_dim):
        """Verify existing index has correct dimensions, recreate if not"""
        index_description = pc.describe_index(config.PINECONE_INDEX_NAME)
        existing_dim = index_description.dimension
        
        if existing_dim != embed_dim:
            # Dimension mismatch - recreate index
            pc.delete_index(config.PINECONE_INDEX_NAME)
            
            import time
            time.sleep(5)  # Wait for deletion
            
            self._create_pinecone_index(pc, embed_dim)
        else:
            print(f"✅ Using existing Pinecone index ({existing_dim} dimensions)")
    
    def load_documents(self, directory: str = None) -> List:
        """Load documents from directory"""
        if directory is None:
            directory = config.DATA_DIR
        
        # Check if directory exists
        if not os.path.exists(directory):
            print(f"⚠️  Directory {directory} does not exist. Creating it...")
            os.makedirs(directory, exist_ok=True)
            return []
        
        # Check for files
        files = os.listdir(directory)
        if not files:
            print(f"⚠️  No documents found in {directory}")
            return []
        
        # Use LlamaParse if available, otherwise simple reader
        if config.USE_LLAMA_PARSE and LLAMA_PARSE_AVAILABLE and config.LLAMA_CLOUD_API_KEY:
            return self._load_with_llamaparse(directory)
        else:
            return self._load_with_simple_reader(directory)
    
    def _load_with_simple_reader(self, directory: str) -> List:
        """Load documents using basic PDF extraction"""
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True,
            required_exts=[".pdf", ".txt", ".docx", ".md"]
        )
        return reader.load_data()
    
    def _load_with_llamaparse(self, directory: str) -> List:
        """Load documents using advanced PDF parsing with LlamaParse"""
        # Extract images from PDFs if enabled
        if config.EXTRACT_IMAGES and MULTIMODAL_AVAILABLE:
            self._extract_pdf_images(directory)
        
        # Set up LlamaParse
        parser = LlamaParse(
            api_key=config.LLAMA_CLOUD_API_KEY,
            result_type=config.LLAMA_PARSE_RESULT_TYPE,
            verbose=True,
            language="en"
        )
        
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True,
            required_exts=[".pdf", ".txt", ".docx", ".md"],
            file_extractor={".pdf": parser}
        )
        return reader.load_data()
    
    def _extract_pdf_images(self, directory: str):
        """Extract images from all PDFs in directory"""
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)
            try:
                process_pdf_multimodal(pdf_path)
            except Exception as e:
                print(f"   ⚠️ Could not process {pdf_file}: {e}")
    
    def create_index(self, documents: List = None, force_new: bool = False):
        """Create or load vector index from Pinecone"""
        if self.vector_store is None:
            print("❌ Cloud storage not initialized!")
            return None
        
        if not force_new:
            # Try to load existing index
            index = self._load_existing_index()
            if index:
                return index
        
        # Create new index
        if documents is None:
            documents = self.load_documents()
        
        if not documents:
            print("❌ No documents to index. Please add documents to the data directory.")
            return None
        
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        return self.index
    
    def _load_existing_index(self):
        """Load existing index from Pinecone"""
        try:
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=storage_context
            )
            
            # Check if index is empty
            if self._is_index_empty():
                print("⚠️  Cloud storage is empty. No documents indexed yet.")
                self.index = None
                return None
            
            return self.index
        except Exception as e:
            print(f"⚠️  Could not load existing cloud index: {e}")
            print("No documents in cloud storage yet.")
            self.index = None
            return None
    
    def _is_index_empty(self):
        """Check if Pinecone index is empty"""
        try:
            if hasattr(self.vector_store, '_pinecone_index'):
                stats = self.vector_store._pinecone_index.describe_index_stats()
                return stats.get('total_vector_count', 0) == 0
        except:
            pass
        return False
    
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

