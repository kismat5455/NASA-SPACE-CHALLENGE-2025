"""
Streamlit Web Interface for NASA RAG System
"""
import streamlit as st
import os
import hashlib
from pathlib import Path
from query_engine import QueryEngine
from document_ingestion import DocumentIngestion
import config


# Page configuration
st.set_page_config(
    page_title="NASA Research Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0B3D91;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #FC3D21;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background-color: #0B3D91;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def get_file_hash(file_content):
    """Calculate MD5 hash of file content"""
    return hashlib.md5(file_content).hexdigest()


def load_document_metadata():
    """Load metadata of ingested documents"""
    metadata_file = Path(config.DATA_DIR) / ".document_metadata.txt"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            return set(line.strip() for line in f.readlines())
    return set()


def save_document_metadata(file_hash):
    """Save document hash to metadata"""
    metadata_file = Path(config.DATA_DIR) / ".document_metadata.txt"
    with open(metadata_file, 'a') as f:
        f.write(f"{file_hash}\n")


@st.cache_resource
def load_query_engine():
    """Load the query engine (cached)"""
    try:
        engine = QueryEngine()
        return engine
    except Exception as e:
        st.error(f"Error loading query engine: {e}")
        return None


def reload_query_engine():
    """Force reload of query engine after ingestion"""
    st.cache_resource.clear()
    return load_query_engine()


def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<div class="main-header">🚀 NASA Research Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">NASA Space Challenge 2025 - RAG System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=200)
        st.header("About")
        st.write("""
        This RAG (Retrieval-Augmented Generation) system helps you search and query NASA research documents.
        
        **Powered by:**
        - 🧠 Gemini 2.0 Flash
        - 📚 Stella v5 Embeddings
        - 🔍 LlamaParse + Vector Search
        """)
        
        st.divider()
        
        st.header("📤 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload NASA documents",
            type=["pdf", "txt", "docx", "md"],
            accept_multiple_files=True,
            help="Supported: PDF, TXT, DOCX, MD"
        )
        
        if uploaded_files:
            if st.button("🚀 Ingest Documents"):
                with st.spinner("Processing documents..."):
                    ingested_count = 0
                    skipped_count = 0
                    existing_hashes = load_document_metadata()
                    
                    for uploaded_file in uploaded_files:
                        # Calculate file hash to detect duplicates
                        file_content = uploaded_file.read()
                        file_hash = get_file_hash(file_content)
                        
                        if file_hash in existing_hashes:
                            st.warning(f"⚠️ '{uploaded_file.name}' already ingested (duplicate detected)")
                            skipped_count += 1
                            continue
                        
                        # Save file to data directory
                        file_path = Path(config.DATA_DIR) / uploaded_file.name
                        with open(file_path, 'wb') as f:
                            f.write(file_content)
                        
                        # Save metadata
                        save_document_metadata(file_hash)
                        ingested_count += 1
                        st.success(f"✅ Saved '{uploaded_file.name}'")
                    
                    # Re-index if new documents were added
                    if ingested_count > 0:
                        st.info("🔨 Re-indexing documents...")
                        try:
                            ingestion = DocumentIngestion()
                            ingestion.create_index(force_new=True)
                            st.success(f"✅ Successfully ingested {ingested_count} new document(s)!")
                            if skipped_count > 0:
                                st.info(f"ℹ️ Skipped {skipped_count} duplicate(s)")
                            
                            # Reload query engine
                            st.cache_resource.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error during ingestion: {e}")
                    else:
                        st.info("ℹ️ No new documents to ingest")
        
        st.divider()
        
        st.header("Settings")
        top_k = st.slider("Number of sources to retrieve", 1, 10, config.TOP_K_RESULTS)
        
        st.divider()
        
        st.header("System Status")
        if config.GOOGLE_API_KEY:
            st.success("✅ API Key configured")
        else:
            st.error("❌ API Key missing")
        
        # Show document count
        data_dir = Path(config.DATA_DIR)
        if data_dir.exists():
            doc_count = len([f for f in data_dir.iterdir() if f.suffix in ['.pdf', '.txt', '.docx', '.md']])
            st.info(f"📄 {doc_count} document(s) in index")
    
    # Check if API key is configured
    if not config.GOOGLE_API_KEY:
        st.error("⚠️ Google API Key not found! Please configure your .env file.")
        st.code("GOOGLE_API_KEY=your_api_key_here", language="bash")
        return
    
    # Load query engine
    with st.spinner("Loading query engine..."):
        engine = load_query_engine()
    
    if not engine or not engine.query_engine:
        st.warning("⚠️ No document index found. Please run document ingestion first.")
        st.code("python document_ingestion.py", language="bash")
        return
    
    st.success("✅ System ready!")
    
    # Main content area
    st.divider()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Only show sources if they exist, are relevant, and answer was successful
            if "sources" in message and message["sources"]:
                # Filter sources with relevance > 0.3 (adjustable threshold)
                relevant_sources = [s for s in message["sources"] if s.get('score', 0) > 0.3]
                # Check if answer indicates inability to respond
                unable_to_answer = any(phrase in message["content"].lower() for phrase in 
                    ["unable to answer", "cannot answer", "don't have", "not able to"])
                
                if relevant_sources and not unable_to_answer:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(relevant_sources, 1):
                            st.markdown(f"**Source {i}** (Relevance: {source['score']:.2f})")
                            if 'file_name' in source['metadata']:
                                st.caption(f"📄 {source['metadata']['file_name']}")
                            st.text(source['text'])
                            st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about NASA research..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                result = engine.query(prompt)
                
                # Display response
                st.markdown(result["response"])
                
                # Display sources only if they're relevant and answer is useful
                if result["sources"]:
                    # Filter sources with relevance > 0.3 (adjustable threshold)
                    relevant_sources = [s for s in result["sources"] if s.get('score', 0) > 0.3]
                    # Check if answer indicates inability to respond
                    unable_to_answer = any(phrase in result["response"].lower() for phrase in 
                        ["unable to answer", "cannot answer", "don't have", "not able to"])
                    
                    if relevant_sources and not unable_to_answer:
                        with st.expander("📚 View Sources"):
                            for i, source in enumerate(relevant_sources, 1):
                                st.markdown(f"**Source {i}** (Relevance: {source['score']:.2f})")
                                if 'file_name' in source['metadata']:
                                    st.caption(f"📄 {source['metadata']['file_name']}")
                                st.text(source['text'])
                                st.divider()
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"],
                    "sources": result["sources"]
                })
    
    # Clear chat button in sidebar
    with st.sidebar:
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()

