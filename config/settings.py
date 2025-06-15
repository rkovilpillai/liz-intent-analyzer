import os

# Authentication settings
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    'openid', 
    'https://www.googleapis.com/auth/userinfo.email', 
    'https://www.googleapis.com/auth/userinfo.profile'
]
REDIRECT_URI = 'http://localhost:8501/'

# API settings
N8N_WEBHOOK_URL_BASIC = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"
N8N_WEBHOOK_URL_CAMPAIGN = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"

# File paths
AUTH_STORAGE_FILE = '.streamlit_auth.json'

# UI settings
SIDEBAR_WIDTH = "20%"
MAIN_CONTENT_WIDTH = "80%"