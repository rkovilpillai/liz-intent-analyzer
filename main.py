# main.py
import streamlit as st
from auth.google_auth import check_authentication, show_login_page
from components.sidebar import render_sidebar
from components.main_content import render_main_content
from styles import load_styles
from utils.session_state import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="🔮 Contextual Article Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application flow with authentication."""
    
    # Load styles
    load_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Check authentication status
    if check_authentication():
        # User is authenticated - show the app
        render_sidebar()
        render_main_content()
    else:
        # User is not authenticated - show login page
        show_login_page()

if __name__ == '__main__':
    main()