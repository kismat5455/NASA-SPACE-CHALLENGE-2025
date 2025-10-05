"""
UI Components for NASA Research Assistant
Handles styling, themes, and visual elements
"""
import streamlit as st
from pathlib import Path


def setup_page_config():
    """Set up the page - title, icon, layout, etc."""
    st.set_page_config(
        page_title="NASA Research Assistant",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo',
            'Report a bug': 'https://github.com/your-repo/issues',
            'About': "Alexi Research Assistant - Built for NASA Space Challenge 2025 - Winnipeg,MB"
        }
    )


def apply_dark_theme():
    """Apply the NASA-inspired dark theme to the app"""
    st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Main container */
    .main .block-container {
        background-color: #1e2130;
        padding: 2rem;
        max-width: 100%;
    }
    
    /* NASA-style header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #262730;
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    
    /* Add padding to sidebar content to prevent overlap with fixed button */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-bottom: 120px;
    }
    
    /* Sticky chat footer section */
    .chat-footer-section {
        position: sticky;
        bottom: 0;
        background-color: #262730;
        padding: 1rem 0;
        border-top: 2px solid #4A90E2;
        margin-top: 2rem;
        z-index: 100;
        box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Ensure sidebar content can scroll without overlapping footer */
    [data-testid="stSidebar"] section {
        padding-bottom: 140px !important;
    }
    
    /* Sidebar text styling */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h3 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] img {
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #4A90E2;
        background-color: #2d3250;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #4A90E2;
        border-color: #4A90E2;
    }
    
    .stButton>button[kind="primary"] {
        background-color: #4A90E2;
        border-color: #4A90E2;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #2d3250;
        border-radius: 8px;
        border-left: 3px solid #4A90E2;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* User messages */
    [data-testid="stChatMessageContent"] {
        color: #ffffff;
    }
    
    /* Input fields */
    .stTextInput input, .stChatInput input {
        background-color: #2d3250;
        color: #ffffff;
        border: 1px solid #4A90E2;
        border-radius: 8px;
    }
    
    .stTextInput input::placeholder {
        color: #8b92a8;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #2d3250;
        border-radius: 8px;
        border: 1px dashed #4A90E2;
        padding: 1rem;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #1e4620;
        color: #7ed987;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    
    .stInfo {
        background-color: #1e3a5f;
        color: #74b9ff;
        border-radius: 8px;
        border-left: 4px solid #4A90E2;
    }
    
    .stWarning {
        background-color: #5f4a1e;
        color: #ffd97d;
        border-radius: 8px;
        border-left: 4px solid #ffa500;
    }
    
    .stError {
        background-color: #5f1e1e;
        color: #ff9999;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2d3250;
        color: #ffffff;
        border-radius: 8px;
    }
    
    /* Divider */
    hr {
        border-color: #4A90E2;
        opacity: 0.3;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #4A90E2;
    }
    
    /* General text */
    p, span, label, .stMarkdown {
        color: #e0e0e0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


def show_nasa_logo():
    """Display the NASA logo in the sidebar, or a rocket emoji as fallback"""
    try:
        logo_path = Path("assets/nasa_logo.png")
        if logo_path.exists():
            st.image(str(logo_path), width=150)
        else:
            # If logo file doesn't exist, show emoji
            st.markdown("# 🚀")
    except:
        # If anything goes wrong, just show the emoji
        st.markdown("# 🚀")


def render_header():
    """Show the main header with title and subtitle"""
    st.markdown('<div class="main-header">🚀 Alexi Research Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Built for NASA Space Challenge 2025 - Winnipeg, MB</div>', unsafe_allow_html=True)


def validate_url(url):
    """
    Check if a URL is valid (starts with http:// or https://)
    
    Args:
        url: The URL string to check
        
    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False
    url = url.strip()
    return url.startswith(('http://', 'https://'))

