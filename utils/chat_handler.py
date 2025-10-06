"""
Chat Handler for NASA Research Assistant
Manages chat display, source citations, and image rendering
"""
import streamlit as st
from pathlib import Path
from utils.document_manager import load_document_metadata


def display_chat_message(message):
    """
    Display a single chat message with sources and images
    
    Args:
        message: Message dict with role, content, sources, images
    """
    role = message["role"]
    content = message["content"]
    
    # Choose the right avatar
    avatar = "👤" if role == "user" else "🤖"
    
    with st.chat_message(role, avatar=avatar):
        # Show the message text
        st.markdown(content)
        
        # If it's an assistant message, show images and sources
        if role == "assistant":
            _display_images(message)
            _display_sources(message, content)


def _display_images(message):
    """Show any images attached to this message"""
    if "images" not in message or not message["images"]:
        return
    
    st.markdown("")  # Add some spacing
    
    for img_data in message["images"]:
        try:
            img_path = Path(img_data["path"])
            if not img_path.exists():
                continue
            
            # Show the image
            st.image(str(img_path), use_column_width=True)
            
            # Add caption with source info
            caption_parts = []
            if "source_pdf" in img_data:
                caption_parts.append(f"📄 {img_data['source_pdf']}")
            if "page" in img_data:
                caption_parts.append(f"Page {img_data['page']}")
            
            if caption_parts:
                st.caption(" • ".join(caption_parts))
            
            # Show image description if available
            if "description" in img_data and img_data["description"]:
                with st.expander("📋 Image details"):
                    st.write(img_data["description"])
            
            st.markdown("")  # Spacing after each image
        except:
            # Skip images that can't be displayed
            pass


def _display_sources(message, content):
    """Show the source citations for this message"""
    if "sources" not in message or not message["sources"]:
        return
    
    relevant_sources = message["sources"]
    
    # Don't show sources if the assistant says they don't have info
    no_info_phrases = [
        "don't have specific information",
        "don't have information",
        "no information available",
        "not available in",
        "cannot find"
    ]
    
    has_no_info = any(phrase in content.lower() for phrase in no_info_phrases)
    
    if not relevant_sources or has_no_info:
        return
    
    # Display sources section
    st.markdown("---")
    st.caption("**📚 Sources:**")
    
    metadata = load_document_metadata()
    
    # Get unique source documents
    unique_sources = {}
    for source in relevant_sources:
        filename = source['metadata'].get('file_name', 'Unknown')
        if filename not in unique_sources:
            unique_sources[filename] = True
    
    # Show each source with link if available, numbered like [1], [2], etc.
    for idx, filename in enumerate(unique_sources.keys(), 1):
        doc_url = None
        
        # Find the URL for this document
        for hash_val, meta in metadata.items():
            if meta.get('filename') == filename:
                doc_url = meta.get('url')
                break
        
        # Display with numbered citation and clickable link (just the URL)
        if doc_url:
            st.markdown(f"[{idx}] [{doc_url}]({doc_url})")
        else:
            st.markdown(f"[{idx}] {filename}")


def display_chat_history():
    """Display all messages from the chat history"""
    for message in st.session_state.messages:
        display_chat_message(message)


def get_chat_input():
    """
    Show the chat input box and return user input
    
    Returns:
        User's question string, or None if no input
    """
    return st.chat_input(
        "Ask a question about NASA research...",
        key="main_chat_input"
    )

