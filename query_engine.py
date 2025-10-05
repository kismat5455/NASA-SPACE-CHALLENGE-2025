"""
Query Engine Module for NASA RAG System
Handles querying the indexed documents
"""
import os
import warnings

# Suppress Google gRPC warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
warnings.filterwarnings('ignore', category=DeprecationWarning)

from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Cloud storage imports
try:
    from pinecone import Pinecone
    from llama_index.vector_stores.pinecone import PineconeVectorStore
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

import config
from document_ingestion import DocumentIngestion


class QueryEngine:
    """Handles querying the NASA document index"""
    
    def __init__(self, starting_model_index: int = 0):
        """Initialize the query engine"""
        self.available_models = [config.GEMINI_MODEL] + config.FALLBACK_MODELS
        self.model_index = starting_model_index
        self.current_model = self.available_models[self.model_index]
        
        # Set up AI model and embeddings
        self._setup_llm()
        self._setup_embeddings()
        
        # Initialize cloud storage and load documents
        self.vector_store = None
        self._init_cloud_storage()
        
        self.ingestion = DocumentIngestion()
        self.index = self.ingestion.get_index()
        
        # Create query engine with prompt template
        if self.index:
            self.query_engine = self._create_query_engine()
        else:
            self.query_engine = None
    
    def _setup_llm(self):
        """Set up the language model"""
        Settings.llm = Gemini(
            model=self.current_model,
            api_key=config.GOOGLE_API_KEY,
            temperature=0.7
        )
    
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
    
    def _create_query_engine(self):
        """Create query engine with prompt template"""
        from llama_index.core.prompts import PromptTemplate
        
        qa_prompt = PromptTemplate(
            config.SYSTEM_PROMPT + 
            "\n\n=== CONTEXT FROM NASA RESEARCH PAPERS ===\n"
            "{context_str}\n"
            "=== END OF CONTEXT ===\n\n"
            "IMPORTANT: Use ONLY the information provided in the context above. Do not use external knowledge.\n\n"
            "Question: {query_str}\n\n"
            "Answer (based ONLY on the context above): "
        )
        
        return self.index.as_query_engine(
            similarity_top_k=config.TOP_K_RESULTS,
            response_mode="compact",
            text_qa_template=qa_prompt,
            similarity_cutoff=config.RELEVANCE_THRESHOLD
        )
    
    def _init_cloud_storage(self):
        """Initialize Pinecone cloud vector storage"""
        if not PINECONE_AVAILABLE:
            raise ImportError("Pinecone is required. Install with: pip install pinecone-client llama-index-vector-stores-pinecone")
        
        if not config.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is required in .env file")
        
        try:
            # Initialize Pinecone
            pc = Pinecone(api_key=config.PINECONE_API_KEY)
            
            # Check if index exists
            existing_indexes = [idx.name for idx in pc.list_indexes()]
            
            if config.PINECONE_INDEX_NAME not in existing_indexes:
                # Index doesn't exist - this is OK, it will be created on first upload
                print(f"⚠️  Pinecone index '{config.PINECONE_INDEX_NAME}' doesn't exist yet.")
                print(f"💡 It will be created automatically when you upload your first document.")
                self.vector_store = None
                return
            
            # Connect to existing index
            pinecone_index = pc.Index(config.PINECONE_INDEX_NAME)
            
            # Create LlamaIndex vector store
            self.vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
            
        except Exception as e:
            print(f"❌ Error initializing Pinecone: {e}")
            # Don't raise - allow app to start even if index doesn't exist yet
            self.vector_store = None
    
    def _switch_to_fallback_model(self) -> bool:
        """Switch to the next fallback model if available"""
        self.model_index += 1
        if self.model_index >= len(self.available_models):
            return False
        
        self.current_model = self.available_models[self.model_index]
        self._setup_llm()
        
        # Recreate query engine with new model
        if self.index:
            self.query_engine = self._create_query_engine()
        
        return True
    
    def _is_quota_error(self, error: Exception) -> bool:
        """Check if error is related to quota/rate limiting"""
        error_str = str(error).lower()
        quota_indicators = [
            "quota",
            "rate limit",
            "resource exhausted",
            "429",
            "too many requests",
            "limit exceeded"
        ]
        return any(indicator in error_str for indicator in quota_indicators)
    
    def query(self, question: str, on_model_switch=None) -> dict:
        """Query documents with automatic fallback on errors"""
        # No documents uploaded yet
        if not self.query_engine:
            return self._no_documents_response()
        
        max_retries = len(self.available_models)
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = self.query_engine.query(question)
                
                # Check for empty response
                if not str(response).strip():
                    return self._no_documents_response()
                
                # Extract sources and images
                sources, source_documents = self._extract_sources(response)
                relevant_images = self._get_images_for_sources(source_documents)
                
                return {
                    "response": str(response),
                    "sources": sources,
                    "images": relevant_images
                }
                
            except Exception as e:
                last_error = e
                
                # Try fallback model if it's a quota error
                if self._is_quota_error(e) and attempt < max_retries - 1:
                    if self._switch_to_fallback_model():
                        if on_model_switch:
                            on_model_switch(self.model_index)
                        continue
                    else:
                        break
                else:
                    break
        
        # Return friendly error message
        return self._error_response(last_error)
    
    def _no_documents_response(self):
        """Response when no documents are uploaded"""
        return {
            "response": "Hi there! 👋 I'm **Alexi**, your AI research assistant built for the NASA Space Challenge 2025 in Winnipeg! 🚀\n\nI'm designed to help you explore and understand NASA research papers, but I need some documents to work with first!\n\n### 📤 To get started:\n\n1. **Upload PDF documents** using the sidebar on the left\n2. I'll analyze them and be ready to answer your questions!\n\n### 💡 What I can do:\n- Answer questions about your NASA research papers\n- Find specific information across multiple documents\n- Explain complex scientific concepts\n- Show relevant images and figures from the papers\n\nOnce you upload some documents, just ask me anything about them! I'm here to help make space research more accessible. 🌟",
            "sources": [],
            "images": []
        }
    
    def _extract_sources(self, response):
        """Extract relevant sources from query response"""
        sources = []
        source_documents = set()
        
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                if node.score >= config.RELEVANCE_THRESHOLD:
                    sources.append({
                        "text": node.node.text[:200] + "...",
                        "score": node.score,
                        "metadata": node.node.metadata
                    })
                    
                    if 'file_name' in node.node.metadata:
                        source_documents.add(node.node.metadata['file_name'])
        
        return sources, source_documents
    
    def _error_response(self, error):
        """Generate user-friendly error response"""
        if self._is_quota_error(error):
            return {
                "response": "I apologize, but I'm experiencing high traffic right now and my API quota has been temporarily exceeded. 😅 This usually resolves quickly! In the meantime, you can:\n\n1. Try again in a few minutes\n2. Ask a simpler question that requires less processing\n3. Check back later when the quota resets\n\nI'm still here to help as soon as the quota refreshes! 🚀",
                "sources": [],
                "images": []
            }
        else:
            return {
                "response": "I encountered an unexpected issue while processing your question. 🤔 This could be temporary! Please try:\n\n1. Rephrasing your question\n2. Asking something more specific\n3. Checking back in a moment\n\nI'm here to help and will be back to normal soon! 🚀",
                "sources": [],
                "images": []
            }
    
    
    def _get_images_for_sources(self, source_documents: set) -> list:
        """Get relevant images from source documents"""
        import json
        from pathlib import Path
        
        images = []
        image_metadata_file = Path(config.IMAGE_EXTRACTION_DIR) / "image_metadata.json"
        
        if not image_metadata_file.exists():
            return images
        
        try:
            with open(image_metadata_file, 'r', encoding='utf-8') as f:
                all_images = json.load(f)
            
            # Filter images by source documents
            for img_data in all_images:
                source_pdf = img_data.get('source_pdf', '')
                source_name = source_pdf.replace('.pdf', '')
                
                # Check if image is from a relevant source
                for doc_name in source_documents:
                    if source_name in doc_name or doc_name in source_name:
                        images.append(img_data)
                        break
            
            return images[:3]  # Top 3 images only
            
        except Exception as e:
            print(f"⚠️ Could not load image metadata: {e}")
            return []
    
    def chat(self):
        """Interactive chat mode"""
        if not self.query_engine:
            print("❌ No index available. Please run document_ingestion.py first.")
            return
        
        print("\n" + "=" * 60)
        print("NASA Document Research Assistant")
        print("=" * 60)
        print("Ask questions about NASA research documents")
        print("Type 'exit' or 'quit' to end the session")
        print("=" * 60 + "\n")
        
        while True:
            try:
                question = input("🚀 You: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                result = self.query(question)
                
                print(f"\n🤖 Assistant: {result['response']}\n")
                
                if result['sources']:
                    print("📚 Sources:")
                    for i, source in enumerate(result['sources'], 1):
                        print(f"\n  [{i}] (Relevance: {source['score']:.2f})")
                        if 'file_name' in source['metadata']:
                            print(f"      File: {source['metadata']['file_name']}")
                        print(f"      Preview: {source['text']}")
                
                print("\n" + "-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    """Main function to run the query engine"""
    # Check if API key is set
    if not config.GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in .env file")
        print("Please create a .env file with your Gemini API key")
        return
    
    # Initialize and start chat
    engine = QueryEngine()
    engine.chat()


if __name__ == "__main__":
    main()

