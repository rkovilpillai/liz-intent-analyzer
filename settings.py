# config/settings.py
import os

# Simple environment detection
def is_production():
    """Detect if running in Streamlit Cloud"""
    return (
        os.path.exists("/mount/src") or  # Streamlit Cloud path
        "STREAMLIT_CLOUD" in os.environ or
        os.environ.get("STREAMLIT_SHARING_MODE") == "running"
    )

# Authentication settings - simplified
CLIENT_SECRETS_FILE = "client_secret.json"  # Only used locally
SCOPES = [
    'openid', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile'
]
REDIRECT_URI = 'http://localhost:8501/'  # Will be overridden in auth file

# API settings - keep your existing ones
N8N_WEBHOOK_URL_BASIC = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"
N8N_WEBHOOK_URL_CAMPAIGN = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"

# File paths
AUTH_STORAGE_FILE = '.streamlit_auth.json'

# UI settings
SIDEBAR_WIDTH = "20%"
MAIN_CONTENT_WIDTH = "80%"