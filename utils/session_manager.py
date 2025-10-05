"""
Session State Manager for NASA Research Assistant
Keeps track of chat history, uploads, and user state
"""
import streamlit as st


def initialize_session_state():
    """
    Set up all the session variables we need
    This runs once when the app starts
    """
    # Chat messages history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Document URLs mapping (filename -> URL)
    if 'doc_urls' not in st.session_state:
        st.session_state.doc_urls = {}
    
    # Count how many queries the user has made
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    
    # Show welcome message on first load
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    
    # Track which AI model we're currently using (for fallback handling)
    if 'current_model_index' not in st.session_state:
        st.session_state.current_model_index = 0


def clear_chat_history():
    """Wipe the chat history and start fresh"""
    st.session_state.messages = []
    st.session_state.query_count = 0


def add_message(role, content, sources=None, images=None):
    """
    Add a message to the chat history
    
    Args:
        role: 'user' or 'assistant'
        content: The message text
        sources: List of source documents (optional)
        images: List of relevant images (optional)
    """
    message = {
        "role": role,
        "content": content,
    }
    
    # Add sources if provided
    if sources is not None:
        message["sources"] = sources
    
    # Add images if provided
    if images is not None:
        message["images"] = images
    
    st.session_state.messages.append(message)

