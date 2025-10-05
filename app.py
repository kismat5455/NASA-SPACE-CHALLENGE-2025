"""
NASA Research Assistant - Production Web Interface
A RAG system for querying NASA research documents using Gemini 2.0 and LlamaParse
"""
import streamlit as st
from pathlib import Path

# Import our core modules
from query_engine import QueryEngine
from document_ingestion import DocumentIngestion
from multimodal_processor import process_pdf_multimodal
import config

# Import utility functions (keeps the code clean!)
from utils import (
    setup_page_config,
    apply_dark_theme,
    validate_url,
    show_nasa_logo,
    render_header,
    initialize_session_state,
    clear_chat_history,
    add_message,
    get_file_hash,
    load_document_metadata,
    save_document_metadata,
    add_document_to_metadata,
    display_chat_history,
    get_chat_input,
)


# Set up the page and apply styling
setup_page_config()
apply_dark_theme()


# Utility functions are now in the utils/ directory!


@st.cache_resource
def load_query_engine(_model_index=0):
    """Load the query engine (cached) with error handling
    
    Args:
        _model_index: Starting model index (underscore prevents hashing for cache key)
    """
    try:
        engine = QueryEngine(starting_model_index=_model_index)
        if not engine or not engine.query_engine:
            return None
        return engine
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading query engine: {str(e)}")
        return None


def reload_query_engine():
    """Force reload of query engine after ingestion"""
    st.cache_resource.clear()
    # Reset model index on reload
    if 'current_model_index' in st.session_state:
        return load_query_engine(st.session_state.current_model_index)
    return load_query_engine()


# Session state initialization moved to utils/session_manager.py


def main():
    """Main Streamlit application with production-ready features"""
    
    # Set up session state and display header
    initialize_session_state()
    render_header()
    
    # Sidebar
    with st.sidebar:
        # Show the NASA logo
        show_nasa_logo()
        
        st.markdown("### About")
        st.markdown("""
        It helps you search and query  research documents using RAG (Retrieval-Augmented Generation).
        """)
        
        # Silently handle fallback models without showing notifications
        
        st.divider()
        
        # Document Upload
        st.markdown("### 📁 Upload Documents")
        
        
        uploaded_file = st.file_uploader(
            "Select PDF file",
            type=["pdf"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            help="Limit 200MB per file • PDF"
        )
        
        # URL input for the uploaded file
        if uploaded_file:
            st.caption(f"📄 {uploaded_file.name}")
            
            url = st.text_input(
                f"URL for {uploaded_file.name}",
                key=f"url_{uploaded_file.name}",
                placeholder="https://...",
                label_visibility="collapsed"
            )
            if url:
                st.session_state.doc_urls[uploaded_file.name] = url
            
            # Ingest button
            ingest_button = st.button("Process & Index", type="primary", use_container_width=True)
            
            if st.button("Cancel", use_container_width=True):
                st.session_state.doc_urls = {}
                st.rerun()
            
            if ingest_button:
                # Validate URL
                url_input = st.session_state.doc_urls.get(uploaded_file.name, "").strip()
                if not validate_url(url_input):
                    st.error("Please provide a valid URL")
                    st.caption("URL must start with http:// or https://")
                else:
                    # Progress container
                    status_container = st.empty()
                    
                    try:
                        with st.spinner("Processing..."):
                            metadata = load_document_metadata()
                            
                            status_container.info(f"Processing {uploaded_file.name}...")
                            
                            # Calculate file hash to detect duplicates
                            file_content = uploaded_file.read()
                            file_hash = get_file_hash(file_content)
                            
                            if file_hash in metadata:
                                status_container.warning(f"⚠️ {uploaded_file.name} already indexed")
                            else:
                                # Save file to data directory
                                file_path = Path(config.DATA_DIR) / uploaded_file.name
                                with open(file_path, 'wb') as f:
                                    f.write(file_content)
                                
                                # Save metadata with URL (using our utility function!)
                                add_document_to_metadata(file_hash, uploaded_file.name, url_input)
                                
                                # Process PDFs with multimodal extraction
                                if config.EXTRACT_IMAGES and file_path.suffix.lower() == '.pdf':
                                    status_container.info("Extracting images...")
                                    try:
                                        multimodal_data = process_pdf_multimodal(str(file_path))
                                        num_images = len(multimodal_data.get('images', []))
                                        if num_images > 0:
                                            status_container.success(f"Extracted {num_images} images")
                                    except Exception as e:
                                        pass
                                
                                # Index documents
                                status_container.info("Creating embeddings...")
                                try:
                                    ingestion = DocumentIngestion()
                                    ingestion.create_index(force_new=True)
                                    status_container.success(f"✅ Successfully indexed {uploaded_file.name}")
                                    
                                    # Clear URLs and reload
                                    st.session_state.doc_urls = {}
                                    st.cache_resource.clear()
                                    st.rerun()
                                except Exception as e:
                                    status_container.error(f"Indexing failed: {str(e)}")
                    
                    except Exception as e:
                        st.error(f"Processing error: {str(e)}")
        
        # Add spacing before footer button
        st.markdown("<div style='padding-bottom: 40px;'></div>", unsafe_allow_html=True)
    
    # Sticky footer container for Clear Chat button
    with st.sidebar:
        # This will be at the bottom due to sticky CSS
        st.markdown('<div class="chat-footer-section">', unsafe_allow_html=True)
        st.markdown("### 💬 Chat")
        
        if st.button("Clear Chat", use_container_width=True, key="clear_chat_btn"):
            clear_chat_history()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if API key is configured
    if not config.GOOGLE_API_KEY:
        st.error("Google API Key not configured")
        st.info("Add `GOOGLE_API_KEY=your_key` to a `.env` file")
        return
    
    # Load query engine with error handling
    try:
        with st.spinner("Loading..."):
            model_idx = st.session_state.get('current_model_index', 0)
            engine = load_query_engine(model_idx)
    except Exception as e:
        st.error(f"Failed to load: {str(e)}")
        return
    
    # Check engine status
    if not engine or not engine.query_engine:
        st.warning("⚠️ No documents indexed yet")
        st.info("📤 Upload PDF documents using the sidebar to get started")
        return
    
    # Main content area
    st.divider()
    
    # Display chat history (now handled by our utility function!)
    display_chat_history()
    
    # Get user input
    prompt = get_chat_input()
    
    if prompt:
        # Hide welcome message after first query
        st.session_state.show_welcome = False
        st.session_state.query_count += 1
        
        # Add user message to chat (using our utility function!)
        add_message("user", prompt)
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get response with error handling
        with st.chat_message("assistant", avatar="🤖"):
            try:
                # Define callback for model switching
                def on_model_switch(new_model_index):
                    st.session_state.current_model_index = new_model_index
                    # Clear cache to reload with new model
                    st.cache_resource.clear()
                
                # Track if model switched during this query
                initial_model = engine.current_model
                
                with st.spinner("Searching..."):
                    result = engine.query(prompt, on_model_switch=on_model_switch)
                
                # Silently handle model switches without showing notifications
                
                # Display response
                st.markdown(result["response"])
                
                # Display relevant images directly in the response
                if result.get("images"):
                    st.markdown("")  # Small spacing
                    for img_data in result["images"]:
                        try:
                            img_path = Path(img_data["path"])
                            if img_path.exists():
                                # Display image prominently
                                st.image(str(img_path), use_column_width=True)
                                # Show compact metadata below image
                                caption_parts = []
                                if "source_pdf" in img_data:
                                    caption_parts.append(f"📄 {img_data['source_pdf']}")
                                if "page" in img_data:
                                    caption_parts.append(f"Page {img_data['page']}")
                                if caption_parts:
                                    st.caption(" • ".join(caption_parts))
                                # Show description if available
                                if "description" in img_data and img_data["description"]:
                                    with st.expander("📋 Image details"):
                                        st.write(img_data["description"])
                                st.markdown("")  # Spacing between images
                        except Exception as e:
                            pass  # Silently skip images that can't be displayed
                
                # Display sources
                if result["sources"]:
                    relevant_sources = result["sources"]
                    no_info_available = any(phrase in result["response"].lower() for phrase in 
                        ["don't have specific information", "don't have information", 
                         "no information available", "not available in", "cannot find"])
                    
                    if relevant_sources and not no_info_available:
                        st.markdown("---")
                        st.caption("**📚 Sources:**")
                        metadata = load_document_metadata()
                        
                        # Get unique sources
                        unique_sources = {}
                        for source in relevant_sources:
                            filename = source['metadata'].get('file_name', 'Unknown')
                            if filename not in unique_sources:
                                unique_sources[filename] = True
                        
                        # Display sources
                        for filename in unique_sources.keys():
                            doc_url = None
                            for hash_val, meta in metadata.items():
                                if meta.get('filename') == filename:
                                    doc_url = meta.get('url')
                                    break
                            
                            if doc_url:
                                st.caption(f"• [{filename}]({doc_url})")
                            else:
                                st.caption(f"• {filename}")
                
                # Add assistant message to chat history (using our utility function!)
                add_message(
                    "assistant", 
                    result["response"],
                    sources=result["sources"],
                    images=result.get("images", [])
                )
                
            except Exception as e:
                # Show user-friendly error message
                error_msg = "I encountered an issue while searching the documents. 🤔 Please try again or rephrase your question!"
                st.warning(error_msg)
                
                # Add error to chat history
                add_message("assistant", error_msg, sources=[], images=[])


if __name__ == "__main__":
    main()

