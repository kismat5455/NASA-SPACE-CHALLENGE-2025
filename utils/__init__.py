"""
Utility modules for NASA Research Assistant
"""

# Make imports easier
from .ui_components import (
    setup_page_config, 
    apply_dark_theme, 
    validate_url, 
    show_nasa_logo,
    render_header
)
from .session_manager import (
    initialize_session_state,
    clear_chat_history,
    add_message
)
from .document_manager import (
    get_file_hash, 
    load_document_metadata, 
    save_document_metadata,
    add_document_to_metadata,
    get_document_url,
    is_document_indexed
)
from .chat_handler import (
    display_chat_message,
    display_chat_history,
    get_chat_input
)

__all__ = [
    # UI Components
    'setup_page_config',
    'apply_dark_theme',
    'validate_url',
    'show_nasa_logo',
    'render_header',
    
    # Session Management
    'initialize_session_state',
    'clear_chat_history',
    'add_message',
    
    # Document Management
    'get_file_hash',
    'load_document_metadata',
    'save_document_metadata',
    'add_document_to_metadata',
    'get_document_url',
    'is_document_indexed',
    
    # Chat Handler
    'display_chat_message',
    'display_chat_history',
    'get_chat_input',
]

