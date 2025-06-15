import streamlit as st

def initialize_session_state():
    # Authentication state
    if 'auth_code' not in st.session_state:
        st.session_state.auth_code = None
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None
    
    # App state
    if 'campaign_analysis' not in st.session_state:
        st.session_state.campaign_analysis = False
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None