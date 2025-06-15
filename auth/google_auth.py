# auth/google_auth.py
import streamlit as st
import json
import os
import webbrowser
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Simple cloud detection
def is_cloud():
    """Detect if running in Streamlit Cloud"""
    return (
        os.path.exists("/mount/src") or  # Streamlit Cloud path
        "STREAMLIT_CLOUD" in os.environ or
        os.environ.get("STREAMLIT_SHARING_MODE") == "running"
    )

# Settings
SCOPES = [
    'openid', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile'
]

def get_redirect_uri():
    """Get redirect URI based on environment"""
    if is_cloud():
        # TODO: Replace 'your-app-name' with your actual Streamlit app name
        return 'https://liz-intent-analyzer-test.streamlit.app/'
    else:
        return 'http://localhost:8501/'

AUTH_STORAGE_FILE = '.streamlit_auth.json'

def get_flow():
    """Create Flow - using secrets in cloud, JSON file locally"""
    redirect_uri = get_redirect_uri()
    
    if is_cloud():
        # In Streamlit Cloud - use secrets
        try:
            client_config = {
                "web": {
                    "client_id": st.secrets["GOOGLE_CLIENT_ID"],
                    "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            }
            return Flow.from_client_config(
                client_config,
                scopes=SCOPES,
                redirect_uri=redirect_uri
            )
        except KeyError as e:
            st.error(f"Missing secret: {e}")
            st.error("Please configure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in Streamlit Cloud secrets")
            st.stop()
    else:
        # Local development - use JSON file
        try:
            return Flow.from_client_secrets_file(
                "client_secret.json",
                scopes=SCOPES,
                redirect_uri=redirect_uri
            )
        except FileNotFoundError:
            st.error("client_secret.json not found. Please add your Google OAuth credentials.")
            st.stop()

def save_credentials_to_file(credentials_dict):
    try:
        with open(AUTH_STORAGE_FILE, 'w') as f:
            json.dump(credentials_dict, f)
    except Exception as e:
        if not is_cloud():  # Only show error locally
            st.error(f"Failed to save credentials: {e}")

def load_credentials_from_file():
    try:
        if os.path.exists(AUTH_STORAGE_FILE):
            with open(AUTH_STORAGE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        if not is_cloud():  # Only show error locally
            st.error(f"Failed to load credentials: {e}")
    return None

def delete_credentials_file():
    try:
        if os.path.exists(AUTH_STORAGE_FILE):
            os.remove(AUTH_STORAGE_FILE)
    except Exception as e:
        if not is_cloud():  # Only show error locally
            st.error(f"Failed to delete credentials: {e}")

def handle_oauth_callback():
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
    try:
        flow = get_flow()
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        if is_cloud():
            # In cloud - provide link (webbrowser doesn't work)
            st.markdown(f"[🚀 Click here to login with Google]({authorization_url})")
            st.info("After logging in, you'll be redirected back to this app.")
        else:
            # Local - open in browser
            webbrowser.open_new_tab(authorization_url)
    except Exception as e:
        st.error(f"Login failed: {e}")

def logout_user():
    st.session_state.credentials = None
    st.session_state.auth_code = None
    delete_credentials_file()
    st.query_params.clear()
    st.rerun()

def check_authentication():
    if not st.session_state.credentials:
        saved_credentials = load_credentials_from_file()
        if saved_credentials:
            st.session_state.credentials = saved_credentials
    
    handle_oauth_callback()
    return st.session_state.credentials is not None

def show_login_page():
    st.markdown('<h1 class="main-header">🔐 Authentication Required</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Please login with Google to access the Contextual Article Analyzer</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
            <div style="text-align: center; margin: 3rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔮</div>
                <h2 style="color: #f7c3dc; margin-bottom: 1rem;">Welcome to Article Analyzer</h2>
                <p style="color: #9CA3AF; margin-bottom: 2rem;">Liz-powered content intelligence with campaign analysis</p>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🚀 Login with Google", type="primary", use_container_width=True):
            login_button_clicked()
            if not is_cloud():
                st.info("Check your browser for Google login. After logging in, you'll be redirected back here.")