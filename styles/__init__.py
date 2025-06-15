# ===== COMPLETE styles/__init__.py =====

import streamlit as st

def load_css_content():
    """Load all CSS content including your latest styling"""
    
    css_content = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #181c2b;
        color: #E4E4E4;
        font-family: 'Inter', sans-serif;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #272b39bf;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid #374151;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #9CA3AF;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        margin: 0 0.25rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #374151;
        color: #E4E4E4;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8B5CF6 !important;
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0;
        background: transparent;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    .stApp section[data-testid="stSidebar"],
    .stApp section[data-testid="stSidebar"] > div {
        background-color: rgb(35, 39, 54) !important;
        border-right: 1px solid #374151 !important;
    }

    [data-testid="stSidebar"] > div > div {
        background-color: rgb(35, 39, 54) !important;
    }

    [data-testid="stWidgetLabel"] * {
        color: #ffc8c8 !important;
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
        font-size: 1.5rem;
        font-weight: 600;
        color: #CD574C;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Logout section styling */
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
    
    .summary-card {
        background: linear-gradient(135deg, #272b39bf 0%, #2A2A3E 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .summary-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #D1D5DB;
        font-weight: 400;
    }
    
    /* Enhanced video waiting state styling */
    .waiting-state {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: calc(100vh - 8rem);
        min-height: 600px;
        width: 100%;
        overflow: hidden;
        padding: 0;
        margin: 0;
    }

    .video__bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
    }

    .audiences-home-page__content {
        position: fixed;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
        padding: 2rem;
    }

    .home-content__wrapper--inner {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        max-width: 800px;
    }

    .home-content__wrapper--flex {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
        text-align: center;
    }

    .home__text {
        margin: 0;
        padding: 1.5rem 2rem;
        max-width: 700px;
        text-align: center;
        line-height: 45px;
        letter-spacing: 12px;
        color: #ffffff;
        font-size: 24px !important;
        font-weight: 700;
        font-family: "Poppins", sans-serif;
        background: #282b38b3;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .home-content__cta__wrapper {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }

    .button.home-content__cta {
        background: rgba(0, 0, 0, 0.2);
        border: 2px solid #ffffff;
        color: #ffffff;
        padding: 15px 30px;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        backdrop-filter: blur(10px);
    }

    .button.home-content__cta:hover {
        background: #ffffff;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 255, 255, 0.2);
    }
    
    /* Streamlit component overrides */
    .stTextInput > div > div > input {
        background: #272b39bf !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea {
        background: #272b39bf !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    }
    
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
    
    .stSelectbox > div > div > select {
        background: #272b39bf !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide Streamlit branding */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Additional CSS classes from your original app */
    .st-emotion-cache-6qob1r {
        position: relative;
        height: 100%;
        width: 100%;
        overflow: overlay;
        background-color: #181c2b;
    }
    
    .st-emotion-cache-1f3w014 {
        vertical-align: middle;
        overflow: hidden;
        color: inherit;
        fill: rgb(205 87 76);
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        font-size: 5rem;
        width: 1.5rem;
        height: 1.5rem;
        flex-shrink: 0;
    }
    
    .st-emotion-cache-1xulwhk {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #CD574C;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .st-emotion-cache-p7i6r9 {
        font-family: "Source Sans Pro", sans-serif;
        font-size: 1rem;
        color: rgb(253 253 253);
        font-weight: 900;
    }
    
    .st-emotion-cache-169dgwr {
        z-index: 999990;
        color: rgb(255 255 255 / 60%);
        margin-top: 0.25rem;
    }
    
    .st-emotion-cache-102y9h7 {
        font-family: "Source Sans Pro", sans-serif;
        font-size: 1rem;
        margin-bottom: -1rem;
        color: #cd574c;
    }
    """
    
    return css_content

def load_styles():
    """Load all CSS styles into Streamlit"""
    css_content = load_css_content()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)