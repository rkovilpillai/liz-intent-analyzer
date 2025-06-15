import streamlit as st
import json
import os
import webbrowser
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from config.settings import CLIENT_SECRETS_FILE, SCOPES, REDIRECT_URI, AUTH_STORAGE_FILE

def get_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def save_credentials_to_file(credentials_dict):
    try:
        with open(AUTH_STORAGE_FILE, 'w') as f:
            json.dump(credentials_dict, f)
    except Exception as e:
        st.error(f"Failed to save credentials: {e}")

def load_credentials_from_file():
    try:
        if os.path.exists(AUTH_STORAGE_FILE):
            with open(AUTH_STORAGE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Failed to load credentials: {e}")
    return None

def delete_credentials_file():
    try:
        if os.path.exists(AUTH_STORAGE_FILE):
            os.remove(AUTH_STORAGE_FILE)
    except Exception as e:
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
    flow = get_flow()
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    webbrowser.open_new_tab(authorization_url)

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
            st.info("Check your browser for Google login. After logging in, you'll be redirected back here.")