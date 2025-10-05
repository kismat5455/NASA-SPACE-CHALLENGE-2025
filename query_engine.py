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

from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import config
from document_ingestion import DocumentIngestion


class QueryEngine:
    """Handles querying the NASA document index"""
    
    def __init__(self):
        """Initialize the query engine"""
        # Set up LlamaIndex with Gemini
        Settings.llm = Gemini(
            model=config.GEMINI_MODEL,
            api_key=config.GOOGLE_API_KEY,
            temperature=0.7
        )
        
        # Use local embeddings if enabled, otherwise use Google embeddings
        if config.USE_LOCAL_EMBEDDINGS:
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
            Settings.embed_model = GeminiEmbedding(
                model_name=config.EMBEDDING_MODEL,
                api_key=config.GOOGLE_API_KEY
            )
        
        # Load the index
        self.ingestion = DocumentIngestion()
        self.index = self.ingestion.get_index()
        
        if self.index:
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=config.TOP_K_RESULTS,
                response_mode="compact"
            )
        else:
            self.query_engine = None
    
    def query(self, question: str) -> dict:
        """
        Query the NASA documents
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing the response and metadata
        """
        if not self.query_engine:
            return {
                "response": "No index available. Please run document_ingestion.py first.",
                "sources": []
            }
        
        print(f"\n🔍 Searching NASA documents for: {question}")
        print("-" * 60)
        
        # Query the index
        response = self.query_engine.query(question)
        
        # Extract sources
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                source_info = {
                    "text": node.node.text[:200] + "...",  # First 200 chars
                    "score": node.score,
                    "metadata": node.node.metadata
                }
                sources.append(source_info)
        
        result = {
            "response": str(response),
            "sources": sources
        }
        
        return result
    
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

