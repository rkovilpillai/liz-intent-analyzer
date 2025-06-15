## Contextual Article Analyzer - Enhanced UX with Sidebar Layout + Google Authentication

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import re
from urllib.parse import urlparse, urlencode
import os
import webbrowser
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from auth.google_auth import check_authentication, show_login_page


# =============================================================================
# AUTHENTICATION FUNCTIONS (Add these at the top)
# =============================================================================

# Authentication Configuration
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = 'http://localhost:8501/'

# Initialize authentication session state
if 'auth_code' not in st.session_state:
    st.session_state.auth_code = None
if 'credentials' not in st.session_state:
    st.session_state.credentials = None

def get_flow():
    """Create and return a Flow instance."""
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def save_credentials_to_file(credentials_dict):
    """Save credentials to a local file for persistence."""
    try:
        with open('.streamlit_auth.json', 'w') as f:
            json.dump(credentials_dict, f)
    except Exception as e:
        st.error(f"Failed to save credentials: {e}")

def load_credentials_from_file():
    """Load credentials from local file."""
    try:
        if os.path.exists('.streamlit_auth.json'):
            with open('.streamlit_auth.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Failed to load credentials: {e}")
    return None

def delete_credentials_file():
    """Delete the credentials file."""
    try:
        if os.path.exists('.streamlit_auth.json'):
            os.remove('.streamlit_auth.json')
    except Exception as e:
        st.error(f"Failed to delete credentials: {e}")

def handle_oauth_callback():
    """Handle the OAuth callback and exchange auth code for tokens."""
    if 'code' in st.query_params:
        st.session_state.auth_code = st.query_params['code']
        st.query_params.clear()
        
        try:
            flow = get_flow()
            flow.fetch_token(code=st.session_state.auth_code)
            
            credentials = flow.credentials
            credentials_dict = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            st.session_state.credentials = credentials_dict
            save_credentials_to_file(credentials_dict)
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")

def login_button_clicked():
    """Initiate the OAuth flow when login button is clicked."""
    flow = get_flow()
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    webbrowser.open_new_tab(authorization_url)

def logout_user():
    """Handle user logout."""
    st.session_state.credentials = None
    st.session_state.auth_code = None
    delete_credentials_file()
    st.query_params.clear()
    st.rerun()

def check_authentication():
    """Check if user is authenticated and handle accordingly."""
    # Check for saved credentials on app start
    if not st.session_state.credentials:
        saved_credentials = load_credentials_from_file()
        if saved_credentials:
            st.session_state.credentials = saved_credentials
    
    # Handle OAuth callback
    handle_oauth_callback()
    
    # Return authentication status
    return st.session_state.credentials is not None

def show_login_page():
    """Display the login page."""
    st.markdown('<h1 class="main-header">🔐 Authentication Required</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Please login with Google to access the Contextual Article Analyzer</p>', unsafe_allow_html=True)
    
    # Center the login content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin: 3rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔮</div>
                <h2 style="color: #f7c3dc; margin-bottom: 1rem;">Welcome to Article Analyzer</h2>
                <p style="color: #9CA3AF; margin-bottom: 2rem;">Liz-powered content intelligence with campaign analysis</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Login with Google", type="primary", use_container_width=True):
            login_button_clicked()
            st.info("Check your browser for Google login. After logging in, you'll be redirected back here.")

# =============================================================================
# YOUR EXISTING APPLICATION FUNCTIONS (Keep all your existing functions)
# =============================================================================

# Page configuration
st.set_page_config(
    page_title="🔮 Contextual Article Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IAB Tier 1 Categories
IAB_TIER1_CATEGORIES = [
    "Arts & Entertainment",
    "Automotive", 
    "Business",
    "Careers",
    "Education",
    "Family & Parenting",
    "Health & Fitness",
    "Food & Drink",
    "Hobbies & Interests",
    "Home & Garden",
    "Law, Government & Politics",
    "News",
    "Personal Finance",
    "Society",
    "Science",
    "Pets",
    "Sports",
    "Style & Fashion",
    "Technology & Computing",
    "Travel",
    "Real Estate",
    "Shopping",
    "Religion & Spirituality",
    "Non-Standard Content"
]

# Function to validate URL format
def is_valid_url(url):
    """Validate URL format before sending to API"""
    if not url or not url.strip():
        return False, "Please enter a URL"
    
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Validate URL format
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)', re.IGNORECASE)
    
    if url_pattern.match(url):
        return True, url
    else:
        return False, "Please enter a valid URL (e.g., https://example.com/article)"

# Function to display error messages with styling
def display_error(error_type, message, suggestions=None, technical_details=None):
    icon = "⚠️"
    color = "#CD574C"

    error_html = f"""
    <div style="margin-top: 1.5rem; color: {color};">
        <h4 style="color: {color}; font-family: Inter; margin-bottom: 0.5rem;">{icon} {message}</h4>
    """
    if suggestions:
        error_html += "<ul style='text-align: left; color: #D1D5DB; line-height: 1.6;'>"
        for s in suggestions:
            error_html += f"<li>{s}</li>"
        error_html += "</ul>"
    if technical_details:
        error_html += f"""
        <details style="margin-top: 1rem; text-align: left;">
            <summary style="color: #9CA3AF; cursor: pointer; font-size: 0.9rem;">Technical Details</summary>
            <div style="margin-top: 0.5rem; padding: 1rem; background: #272b39bf; border-radius: 8px; font-family: monospace; font-size: 0.8rem; color: #9CA3AF;">
                {technical_details}
            </div>
        </details>
        """
    error_html += "</div>"

    st.markdown(error_html, unsafe_allow_html=True)

# Enhanced styling with sidebar layout (keep your existing CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #181c2b;
        color: #E4E4E4;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background: #1f2333 !important;
        border-right: 1px solid #374151;
    }
    
    .css-17lntkn {
        background: #1f2333 !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
    
    .main-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #f7c3dc !important;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #9CA3AF;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .sidebar-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #f7c3dc !important;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-section {
        background: #272b39bf;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    
    .sidebar-section-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #CD574C;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Logout button styling */
    .logout-section {
        background: #272b39bf;
        border: 1px solid #CD574C;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        text-align: center;
    }
    
    .user-info {
        color: #9CA3AF;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Custom logout button */
    .logout-button {
        background: #CD574C !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        cursor: pointer !important;
    }
    
    .logout-button:hover {
        background: #B8503C !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(205, 87, 76, 0.4) !important;
    }
    
    /* Keep all your existing CSS styles here */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #f7c3dc;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.01em;
    }
    
    .content-card {
        background: #272b39bf;
        border: 1px solid #2A2A3E;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .content-card:hover {
        border-color: #374151;
    }
    
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 600;
        color: #CD574C;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    .tag {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        background: #8B5CF6;
        color: #FFFFFF;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .tag:hover {
        background: #7C3AED;
        transform: translateY(-1px);
    }
    
    .tag-secondary {
        background: #CD574C;
        color: #FFFFFF;
    }
    
    .tag-secondary:hover {
        background: #B8503C;
    }
    
    .metric-card {
        background: #272b39bf;
        border: 1px solid #2A2A3E;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #8B5CF6;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.15);
    }
    
    .metric-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #CD574C;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }
    
    /* Keep all your other existing styles... */
    .stButton > button {
        background: #8B5CF6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #7C3AED !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Add more of your existing styles here... */
    
    </style>
""", unsafe_allow_html=True)

# All your existing chart functions (keep these unchanged)
def create_age_chart(demographics):
    # ... keep your existing function
    pass

def create_gender_chart(demographics):
    # ... keep your existing function
    pass

def create_intentionality_chart(intentionality_data):
    # ... keep your existing function
    pass

def create_keyword_chart(primary_kw, secondary_kw):
    # ... keep your existing function
    pass

# Keep all your existing calculation functions
def calculate_intent_accuracy(result):
    # ... keep your existing function
    pass

def calculate_intentionality_score(result):
    # ... keep your existing function
    pass

def get_intentionality_grade(score):
    # ... keep your existing function
    pass

def calculate_content_score(result):
    # ... keep your existing function
    pass

# Initialize session state for your existing app
if 'campaign_analysis' not in st.session_state:
    st.session_state.campaign_analysis = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def your_existing_app():
    """Your existing Streamlit application with authentication-protected content."""
    
    # SIDEBAR - Input Section (20% width) - Your existing sidebar content
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">🔮 Article Analyzer</h2>', unsafe_allow_html=True)
        
        # URL Input Section
        st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-section-title">📄 Article URL</div>
            </div>
        """, unsafe_allow_html=True)
        
        url = st.text_input(
            "Enter article URL",
            placeholder="https://example.com/article",
            help="Enter the full URL of the article you want to analyze",
            label_visibility="collapsed"
        )
        
        # Campaign Toggle Section
        st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-section-title">🎯 Analysis Options</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Real-time toggle with immediate UI updates
        campaign_toggle = st.checkbox(
            "Enable Campaign Relevancy Analysis",
            value=st.session_state.campaign_analysis,
            help="Turn on to analyze how well this content fits your specific campaign objectives"
        )
        
        # Update session state immediately when toggle changes
        if campaign_toggle != st.session_state.campaign_analysis:
            st.session_state.campaign_analysis = campaign_toggle
            st.rerun()
        
        # Campaign fields - appear immediately when toggle is enabled
        campaign_definition = ""
        vertical = ""
        
        if st.session_state.campaign_analysis:
            campaign_definition = st.text_area(
                "Campaign Definition",
                placeholder="e.g., Summer running shoes for marathon training targeting serious athletes aged 25-45",
                help="Describe your campaign objective, target audience, and key messaging",
                height=120
            )
            
            vertical = st.selectbox(
                "Target Vertical (IAB Tier 1)",
                options=[""] + IAB_TIER1_CATEGORIES,
                help="Select the primary industry/vertical for your campaign"
            )
        
        # Dynamic Analyze Button
        if st.session_state.campaign_analysis:
            button_text = "🔍 Analyze Article & Campaign Relevancy"
            button_disabled = not url or not campaign_definition or not vertical
        else:
            button_text = "🔍 Analyze Article Content"
            button_disabled = not url
        
        # Analyze button
        if st.button(button_text, disabled=button_disabled, use_container_width=True):
            # Your existing analysis logic here
            # Validate URL format
            is_valid, processed_url = is_valid_url(url)
            if not is_valid:
                st.error(processed_url)
            else:
                # Start analysis
                st.session_state.analysis_complete = False
                
                # Show appropriate spinner message
                spinner_message = "🔮 Liz - Analyzing content and campaign relevancy..." if st.session_state.campaign_analysis else "🔮 Liz - Analyzing article content..."
                
                with st.spinner(spinner_message):
                    try:
                        # Your existing API call logic here
                        # ... (keep all your existing API logic)
                        pass
                    except Exception as e:
                        st.error(f"Request failed: {e}")
        
        # Help section
        st.markdown("""
            <div class="sidebar-section" style="margin-top: 2rem;">
                <div class="sidebar-section-title">💡 Tips</div>
                <div style="color: #9CA3AF; font-size: 0.875rem; line-height: 1.5;">
                    • Enter a complete article URL<br>
                    • Toggle campaign analysis for deeper insights<br>
                    • Campaign analysis requires both definition and vertical
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ========== AUTHENTICATION SECTION AT BOTTOM ==========
        # User info and logout section at the bottom of sidebar
        if st.session_state.credentials:
            st.markdown("""
                <div class="logout-section">
                    <div class="user-info">✅ Successfully authenticated with Google</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Custom logout button
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                logout_user()

    # MAIN CONTENT AREA - Results Section (80% width) - Your existing main content
    st.markdown('<h1 class="main-header">Contextual Article Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Liz - powered content intelligence with optional campaign analysis</p>', unsafe_allow_html=True)

    # Results Container - Your existing results display logic
    if not st.session_state.analysis_complete or st.session_state.analysis_results is None:
        # Waiting state
        st.markdown("""
            <div class="waiting-state">
                <div class="waiting-icon">🔮</div>
                <div class="waiting-text">Ready to Analyze</div>
                <div class="waiting-subtext">Enter an article URL in the sidebar and click analyze to get started</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display results - Keep all your existing results display logic
        result = st.session_state.analysis_results
        
        # All your existing results display code goes here
        # 📊 CONTENT INTELLIGENCE (Always shown)
        st.markdown('<h2 class="section-header">📊 Content Intelligence</h2>', unsafe_allow_html=True)
        
        # ... Keep all your existing results display logic ...
        # ... (all the existing charts, metrics, summaries, etc.) ...

# =============================================================================
# MAIN APPLICATION FLOW - Authentication Check
# =============================================================================

def main():
    """Main application flow with authentication."""
    
    # Check authentication status
    if check_authentication():
        # User is authenticated - show your existing app
        your_existing_app()
    else:
        # User is not authenticated - show login page
        show_login_page()

if __name__ == '__main__':
    main()