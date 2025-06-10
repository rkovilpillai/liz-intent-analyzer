## Contextual Article Analyzer - Enhanced UX with Sidebar Layout and Tabs

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import re
from urllib.parse import urlparse, urlencode


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

# Enhanced styling with sidebar layout and tabs
st.markdown("""
    <style>
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
        font-size: 1.5rem;
        font-weight: 600;
        color: #CD574C;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
            
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
        fill: currentcolor;
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        font-size: 1.5rem;
        width: 1.5rem;
        height: 1.5rem;
        flex-shrink: 0;
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
    
    .campaign-preview {
        background: linear-gradient(135deg, #272b39bf 0%, #2A2A3E 100%);
        border: 2px solid #8B5CF6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Toggle switch styling */
    .toggle-container {
        background: #272b39bf;
        border: 1px solid #8B5CF6;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Campaign fields styling */
    .campaign-fields {
        background: linear-gradient(135deg, #272b39bf 0%, #2A2A3E 100%);
        border: 1px solid #8B5CF6;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
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
    
    .stSelectbox > div > div > select {
        background: #272b39bf !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
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
    
    /* Sidebar specific button styling */
    .css-1lcbmhc .stButton > button {
        margin-top: 1rem !important;
    }
    
    /* Hide Streamlit branding */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Results area styling */
    .results-container {
        min-height: 80vh;
        background: #181c2b;
    }
    
    /* Main container for waiting state - constrained to main content area */
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

    /* Video background - contained within main content area */
    .video__bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
    }

    /* Content overlay - fixed positioning relative to main area */
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

    /* Logo styling */
    .logo__home {
        margin-bottom: 3rem;
        max-width: 150px;
        height: auto;
        z-index: 11;
    }

    /* Content wrapper */
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

    /* Text styling - fixed and centered */
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

    /* CTA wrapper */
    .home-content__cta__wrapper {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }

    /* Button styling - fixed positioning */
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

    /* Ensure main content area doesn't scroll when video is playing */
    .main .block-container {
        padding-top: 1rem !important;
    }
    section.stSidebar.st-emotion-cache {
        background-color: rgb(35 39 54);
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
    .st-emotion-cache-102y9h7 {
        font-family: "Source Sans Pro", sans-serif;
        font-size: 1rem;
        margin-bottom: -1rem;
        color: #cd574c;
    }         
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    .stApp section[data-testid="stSidebar"],
    .stApp section[data-testid="stSidebar"] > div {
        background-color: rgb(35, 39, 54) !important;
        border-right: 1px solid #374151 !important;
    }

    /* Force all sidebar content to have correct background */

    [data-testid="stSidebar"] > div > div {
        background-color: rgb(35, 39, 54) !important;
    }       
    [data-testid="stWidgetLabel"] * {
        color: #ffc8c8 !important;
    }

    </style>
""", unsafe_allow_html=True)

# All your existing chart functions (keep these unchanged)
def create_age_chart(demographics):
    if not demographics:
        return None
    
    age_distribution = demographics.get('age_distribution', {})
    if not age_distribution:
        return None
    
    # Filter out zero values
    filtered_age_dist = {k: v for k, v in age_distribution.items() if v > 0}
    if not filtered_age_dist:
        return None
    
    age_groups = list(filtered_age_dist.keys())
    percentages = list(filtered_age_dist.values())
    
    # Create vibrant color palette for age groups
    colors = ['#f7c3dc', '#CD574C', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#06B6D4', '#84CC16'][:len(age_groups)]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=age_groups,
        y=percentages,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{p}%" for p in percentages],
        textposition='auto',
        textfont=dict(color="#FFFFFF", size=12, family="Inter")
    ))
    
    fig.update_layout(
        title="Real-Time Age Distribution",
        title_font=dict(color="#f7c3dc", family="Inter", size=16),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#9CA3AF", family="Inter"),
        xaxis=dict(
            gridcolor='rgba(75, 85, 99, 0.3)',
            tickfont=dict(color="#9CA3AF", family="Inter")
        ),
        yaxis=dict(
            gridcolor='rgba(75, 85, 99, 0.3)',
            tickfont=dict(color="#9CA3AF", family="Inter")
        ),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

def create_gender_chart(demographics):
    if not demographics:
        return None
    
    gender_distribution = demographics.get('gender_distribution', {})
    if not gender_distribution:
        return None
    
    genders = list(gender_distribution.keys())
    values = list(gender_distribution.values())
    display_labels = [gender.capitalize() for gender in genders]
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=display_labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=['#f7c3dc', '#CD574C'],
            line=dict(color='#272b39', width=2)
        ),
        textfont=dict(color="#FFFFFF", family="Inter", size=12),
        textinfo='label+percent'
    ))
    
    fig.update_layout(
        title="Real-Time Gender Distribution",
        title_font=dict(color="#f7c3dc", family="Inter", size=16),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#9CA3AF", family="Inter"),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

def create_intentionality_chart(intentionality_data):
    if not intentionality_data:
        return None
    
    # Filter out zero values
    filtered_data = {k: v for k, v in intentionality_data.items() if v > 0}
    if not filtered_data:
        return None
    
    intent_types = [k.capitalize() for k in filtered_data.keys()]
    values = list(filtered_data.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=intent_types,
        fill='toself',
        marker=dict(color='#f7c3dc', size=6),
        line=dict(color='#CD574C', width=2),
        fillcolor='rgba(247, 195, 220, 0.2)',
        name='Intent Distribution'
    ))
    
    fig.update_layout(
        title="Intent Breakdown",
        title_font=dict(color="#f7c3dc", family="Inter", size=16),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) + 10] if values else [0, 100],
                gridcolor='rgba(75, 85, 99, 0.3)',
                tickfont=dict(color="#9CA3AF", family="Inter", size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(75, 85, 99, 0.3)',
                tickfont=dict(color="#9CA3AF", family="Inter", size=11)
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

def create_keyword_chart(primary_kw, secondary_kw):
    if not primary_kw and not secondary_kw:
        return None
    
    labels = primary_kw + secondary_kw
    values = [90] * len(primary_kw) + [60] * len(secondary_kw)
    colors = ['#f7c3dc'] * len(primary_kw) + ['#CD574C'] * len(secondary_kw)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='#272b39', width=2)),
        textfont=dict(color="#ffffff", family="Inter", size=11),
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title="Keyword Distribution",
        title_font=dict(color="#f7c3dc", family="Inter", size=16),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#9CA3AF", family="Inter"),
        showlegend=True,
        legend=dict(
            font=dict(color="#ffffff"),
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        margin=dict(l=40, r=40, t=60, b=60)
    )
    
    return fig

# Performance calculation functions (keep your existing ones)
def calculate_intent_accuracy(result):
    intention = result.get('intention', {})
    confidence = intention.get('confidence', 'low')
    confidence_accuracy = {'high': 85, 'medium': 70, 'low': 50}
    accuracy = confidence_accuracy.get(confidence, 85)
    
    intentionality = result.get('intentionality_breakdown', {})
    if intentionality and any(val > 0 for val in intentionality.values()):
        accuracy += 10
    
    return min(accuracy, 99)

def calculate_intentionality_score(result):
    intentionality = result.get('intentionality_breakdown', {})
    intention = result.get('intention', {})
    confidence = intention.get('confidence', 'medium')
    
    if not intentionality:
        return 0
    
    intent_weights = {
        'transactional': 95,
        'commercial': 75,
        'navigational': 45,
        'informational': 15
    }
    
    weighted_score = 0
    for intent_type, percentage in intentionality.items():
        weight = intent_weights.get(intent_type.lower(), 0)
        weighted_score += (percentage / 100) * weight
    
    confidence_multipliers = {
        'high': 1.0,
        'medium': 0.85,
        'low': 0.7
    }
    
    confidence_multiplier = confidence_multipliers.get(confidence, 0.85)
    final_score = weighted_score * confidence_multiplier
    
    return min(round(final_score), 100)

def calculate_final_intention_score(result, campaign_relevancy=None):
    """
    Calculate the final intention score based on:
    - 80% Campaign Fit Score (if available)
    - 20% Action Intent Score
    
    If campaign analysis is disabled, returns only the Action Intent Score
    """
    # Get the action intent score (intentionality score)
    action_intent_score = calculate_intentionality_score(result)
    
    # If no campaign data, return just the action intent score
    if not campaign_relevancy:
        return action_intent_score, "action_only"
    
    # Get campaign fit score
    campaign_fit_score = campaign_relevancy.get('overall_relevancy_score', 0)
    
    # Calculate weighted final score: 80% campaign fit + 20% action intent
    final_score = (campaign_fit_score * 0.8) + (action_intent_score * 0.2)
    
    return round(final_score), "combined"

def get_final_intention_grade(score, score_type="combined"):
    """
    Get grade and description for the final intention score
    """
    if score_type == "action_only":
        prefix = "Action Intent: "
    else:
        prefix = "Overall Intent: "
    
    if score >= 90:
        return "A+", f"{prefix}Exceptional"
    elif score >= 80:
        return "A", f"{prefix}Excellent"
    elif score >= 70:
        return "B+", f"{prefix}Very Good"
    elif score >= 60:
        return "B", f"{prefix}Good"
    elif score >= 50:
        return "C+", f"{prefix}Fair"
    elif score >= 40:
        return "C", f"{prefix}Below Average"
    elif score >= 30:
        return "D", f"{prefix}Poor"
    else:
        return "F", f"{prefix}Very Poor"

def get_intentionality_grade(score):
    if score >= 85:
        return "A+", "Very High Action Intent"
    elif score >= 75:
        return "A", "High Action Intent"
    elif score >= 65:
        return "B+", "Good Action Intent"
    elif score >= 55:
        return "B", "Moderate Action Intent"
    elif score >= 45:
        return "C+", "Some Action Intent"
    elif score >= 35:
        return "C", "Low Action Intent"
    elif score >= 25:
        return "D", "Very Low Action Intent"
    else:
        return "F", "Minimal Action Intent"

def calculate_content_score(result):
    score = 0
    confidence = result.get('intention', {}).get('confidence', 'Low')
    confidence_scores = {'high': 40, 'medium': 30, 'low': 20}
    score += confidence_scores.get(confidence, 20)
    
    primary_kw = len(result.get('primary_keywords', []))
    secondary_kw = len(result.get('secondary_keywords', []))
    keyword_score = min((primary_kw * 3 + secondary_kw * 2), 20)
    score += keyword_score
    
    tier2_categories = result.get('tier2_categories', [])
    category_score = min(len(tier2_categories) * 5, 15)
    score += category_score
    
    audience_types = result.get('audience_profile', {}).get('type', [])
    interest_groups = result.get('audience_profile', {}).get('interest_groups', [])
    audience_score = min((len(audience_types) * 3 + len(interest_groups) * 2), 15)
    score += audience_score
    
    return min(score, 100)

# Initialize session state
if 'campaign_analysis' not in st.session_state:
    st.session_state.campaign_analysis = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# SIDEBAR - Input Section (20% width)
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
        # Validate URL format
        is_valid, processed_url = is_valid_url(url)
        if not is_valid:
            display_error("invalid_url", processed_url)
        else:
            # Start analysis
            st.session_state.analysis_complete = False
            
            # Show appropriate spinner message
            spinner_message = "🔮 Liz - Analyzing content and campaign relevancy..." if st.session_state.campaign_analysis else "🔮 Liz - Analyzing article content..."
            
            with st.spinner(spinner_message):
                try:
                    # API endpoints
                    n8n_webhook_url_basic = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"
                    n8n_webhook_url_campaign = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine-test"
                    
                    # Choose API endpoint and payload based on toggle
                    if st.session_state.campaign_analysis:
                        # Campaign analysis enabled
                        api_url = n8n_webhook_url_campaign
                        params = {
                            'url': processed_url,
                            'campaign_definition': campaign_definition,
                            'vertical': vertical
                        }
                        encoded_params = urlencode(params)
                        full_api_url = f"{api_url}?{encoded_params}"
                        
                        # Try GET first, then POST
                        response = requests.get(full_api_url, timeout=90)
                        
                        if response.status_code == 200:
                            try:
                                result_data = response.json()
                                
                                # Handle error responses
                                if isinstance(result_data, list) and len(result_data) > 0 and "error" in result_data[0]:
                                    result = result_data[0]
                                    display_error(
                                        error_type=result.get("error_type", "api_error"),
                                        message=result.get("message", "An error occurred during analysis."),
                                        suggestions=result.get("suggestions", []),
                                        technical_details=f"URL: {processed_url}" + (f"\nCampaign: {campaign_definition}\nVertical: {vertical}" if st.session_state.campaign_analysis else "")
                                    )
                                else:
                                    if isinstance(result_data, list):
                                        result = result_data[0]
                                    else:
                                        result = result_data
                                    
                                    # Store results in session state
                                    st.session_state.analysis_results = result
                                    st.session_state.analysis_complete = True
                                    st.rerun()
                                    
                            except Exception as e:
                                display_error(
                                    error_type="parse_error",
                                    message="Failed to process the analysis results",
                                    suggestions=["Try analyzing the article again", "Check if the URL is accessible"],
                                    technical_details=f"Parse error: {str(e)}"
                                )
                        else:
                            display_error(
                                error_type="api_request_failed",
                                message=f"API request failed with status code {response.status_code}",
                                suggestions=[
                                    "Check your internet connection",
                                    "Try again in a few moments",
                                    "Verify the URL is accessible"
                                ],
                                technical_details=f"Response: {response.text[:500]}"
                            )
                    else:
                        api_url = n8n_webhook_url_campaign
                        params = {
                            'url': processed_url
                        }
                        encoded_params = urlencode(params)
                        full_api_url = f"{api_url}?{encoded_params}"
                        
                        # Try GET first, then POST
                        response = requests.get(full_api_url, timeout=90)
                        
                        if response.status_code == 200:
                            try:
                                result_data = response.json()
                                
                                # Handle error responses
                                if isinstance(result_data, list) and len(result_data) > 0 and "error" in result_data[0]:
                                    result = result_data[0]
                                    display_error(
                                        error_type=result.get("error_type", "api_error"),
                                        message=result.get("message", "An error occurred during analysis."),
                                        suggestions=result.get("suggestions", []),
                                        technical_details=f"URL: {processed_url}" + (f"\nCampaign: {campaign_definition}\nVertical: {vertical}" if st.session_state.campaign_analysis else "")
                                    )
                                else:
                                    if isinstance(result_data, list):
                                        result = result_data[0]
                                    else:
                                        result = result_data
                                    
                                    # Store results in session state
                                    st.session_state.analysis_results = result
                                    st.session_state.analysis_complete = True
                                    st.rerun()
                                    
                            except Exception as e:
                                display_error(
                                    error_type="parse_error",
                                    message="Failed to process the analysis results",
                                    suggestions=["Try analyzing the article again", "Check if the URL is accessible"],
                                    technical_details=f"Parse error: {str(e)}"
                                )
                        else:
                            display_error(
                                error_type="api_request_failed",
                                message=f"API request failed with status code {response.status_code}",
                                suggestions=[
                                    "Check your internet connection",
                                    "Try again in a few moments",
                                    "Verify the URL is accessible"
                                ],
                                technical_details=f"Response: {response.text[:500]}"
                            )

                except Exception as e:
                    display_error(
                        error_type="parse_error",
                        message="Failed to process the analysis results",
                        suggestions=["Try analyzing the article again", "Check if the URL is accessible"],
                        technical_details=f"Parse error: {str(e)}"
                    )
    
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

# MAIN CONTENT AREA - Results Section (80% width)
# Results Container
if not st.session_state.analysis_complete or st.session_state.analysis_results is None:
    # Waiting state
    st.markdown("""
        <div class="waiting-state">
            <video loop autoplay muted class="video__bg">
                <source src="https://lizos.seedtag.com/assets/videos/loop_videos/red_network/red_network_loop.webm" type="video/webm">
                Your browser does not support the video tag.
            </video>
            <div class="audiences-home-page__content">
                <div class="home-content__wrapper--inner">
                    <div class="home-content__wrapper--flex">
                        <p class="home__text">My name is LIZ and I'll be your guide around the Contextual Universe, how can I help you?</p>
                        <div class="home-content__cta__wrapper">
                            <div class="button home-content__cta"> ← Enter an article URL in the sidebar to get started</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # Display results with tabs
    result = st.session_state.analysis_results
    
    # Create dynamic tab list based on campaign analysis toggle
    tab_list = ["📊 Overview", "👤 Audience 📈 Insights", "🔑  Keywords",]
    
    # Add campaign tab if campaign analysis is enabled and data exists
    campaign_relevancy = result.get('campaign_relevancy', {})
    if st.session_state.campaign_analysis and campaign_relevancy:
        tab_list.insert(2, "🎯 Campaign")
    
    # Create tabs
    tabs = st.tabs(tab_list)
    
    # TAB 1: OVERVIEW
    with tabs[0]:
        st.markdown('<h2 class="section-header">📊 Content Intelligence Overview</h2>', unsafe_allow_html=True)
        
        # Key metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            intention = result.get('intention', {})
            primary_intent = intention.get('primary', 'Unknown')
            confidence = intention.get('confidence', 'Unknown')
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Intent</div>
                    <div class="metric-value">{primary_intent.title()}</div>
                    <div class="metric-subtitle">
                        <span style="color: #9CA3AF;">{confidence}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            category = result.get('tier1_category', 'Unknown')
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Category</div>
                    <div class="metric-value">{category}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            demographics = result.get('audience_profile', {}).get('demographics', {})
            age_range = demographics.get('age_range', 'Unknown')
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Age Range</div>
                    <div class="metric-value">{age_range}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            income = demographics.get('income_range', 'Unknown')
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Income Range</div>
                    <div class="metric-value">{income}</div>
                </div>
            """, unsafe_allow_html=True)
        
        
        with col5:
            campaign_score = campaign_relevancy.get('overall_relevancy_score', 0) if st.session_state.campaign_analysis and campaign_relevancy else None
            if st.session_state.campaign_analysis and campaign_score is not None:
                # Final Intentionality Score
                final_intentionality_score,score_type = calculate_final_intention_score(result,campaign_relevancy)
                final_grade, final_grade_desc = get_final_intention_grade(final_intentionality_score,score_type)
                intentionality_score = calculate_intentionality_score(result)
                grade, grade_desc = get_intentionality_grade(intentionality_score)
                
                if final_intentionality_score >= 70:
                    score_color = "#10B981"
                elif final_intentionality_score >= 50:
                    score_color = "#F59E0B"
                else:
                    score_color = "#EF4444"
                    
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Intention score</div>
                        <div class="metric-value" style="color: {score_color};">{final_intentionality_score}/100</div>
                        <div class="metric-subtitle">
                            <span style="color: {score_color}; font-weight: 600;">{final_grade}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Intentionality Score
                intentionality_score = calculate_intentionality_score(result)
                grade, grade_desc = get_intentionality_grade(intentionality_score)
                
                if intentionality_score >= 75:
                    score_color = "#10B981"
                elif intentionality_score >= 50:
                    score_color = "#F59E0B"
                else:
                    score_color = "#EF4444"
                    
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Article Intent</div>
                        <div class="metric-value" style="color: {score_color};">{intentionality_score}/100</div>
                        <div class="metric-subtitle">
                            <span style="color: {score_color}; font-weight: 600;">{grade}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Content Summary
        st.markdown('<h3 class="section-header">📝 Summary</h3>', unsafe_allow_html=True)
        
        summary = result.get('summary_rationale', 'No summary available')
        st.markdown(f"""
            <div class="summary-card">
                <div class="summary-text">{summary}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Intentionality Score Explanation
        # Dynamic Intentionality Score Explanation
        campaign_score = campaign_relevancy.get('overall_relevancy_score', 0) if st.session_state.campaign_analysis and campaign_relevancy else None

        if st.session_state.campaign_analysis and campaign_score is not None:
            # Final Intention Score Explanation (Combined Score)
            final_intentionality_score, score_type = calculate_final_intention_score(result, campaign_relevancy)
            final_grade, final_grade_desc = get_final_intention_grade(final_intentionality_score, score_type)
            
            # Calculate individual components for breakdown
            action_intent_score = calculate_intentionality_score(result)
            
            st.markdown(f"""
                <div class="content-card">
                    <div class="card-title">📊 Overall Intention Score Analysis</div>
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 2rem; color: {'#10B981' if final_intentionality_score >= 75 else '#F59E0B' if final_intentionality_score >= 50 else '#EF4444'};">{final_grade}</span>
                            <div>
                                <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">{final_grade_desc}</div>
                                <div style="color: #9CA3AF; font-size: 0.9rem;">Score: {final_intentionality_score}/100</div>
                            </div>
                        </div>
                    </div>
                    <div style="color: #D1D5DB; line-height: 1.5;">
                        <strong>What this means:</strong> This comprehensive score combines campaign relevancy (80%) with user action intent (20%) to predict overall content performance for your specific campaign objectives.
                        <br><br>
                        <strong>Score Breakdown:</strong>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            <li><strong>Campaign Fit:</strong> {campaign_score}/100 (80% weight) - How well the content aligns with your campaign goals</li>
                            <li><strong>Action Intent:</strong> {action_intent_score}/100 (20% weight) - Likelihood of users taking action based on content intent</li>
                        </ul>
                        <br>
                        <strong>Calculation:</strong> ({campaign_score} × 0.8) + ({action_intent_score} × 0.2) = {final_intentionality_score}
                        <br><br>
                        <strong>Content Intent Distribution:</strong>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            {"".join([f"<li><strong>{intent.title()}:</strong> {percent}% (Weight: {['Transactional: 95pts', 'Commercial: 75pts', 'Navigational: 45pts', 'Informational: 15pts'][['transactional', 'commercial', 'navigational', 'informational'].index(intent.lower())]})</li>" for intent, percent in result.get('intentionality_breakdown', {}).items() if percent > 0])}
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Action Intent Score Explanation (Content Analysis Only)
            intentionality_score = calculate_intentionality_score(result)
            grade, grade_desc = get_intentionality_grade(intentionality_score)
            
            st.markdown(f"""
                <div class="content-card">
                    <div class="card-title">📊 Article Intent Score Analysis</div>
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 2rem; color: {'#10B981' if intentionality_score >= 75 else '#F59E0B' if intentionality_score >= 50 else '#EF4444'};">{grade}</span>
                            <div>
                                <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">{grade_desc}</div>
                                <div style="color: #9CA3AF; font-size: 0.9rem;">Score: {intentionality_score}/100</div>
                            </div>
                        </div>
                    </div>
                    <div style="color: #D1D5DB; line-height: 1.5;">
                        <strong>What this means:</strong> This score predicts the likelihood of users taking action (clicking, buying, engaging) based on the article's intent distribution and confidence level.
                        <br><br>
                        <strong>Intent Breakdown:</strong>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            {"".join([f"<li><strong>{intent.title()}:</strong> {percent}% (Weight: {['Transactional: 95pts', 'Commercial: 75pts', 'Navigational: 45pts', 'Informational: 15pts'][['transactional', 'commercial', 'navigational', 'informational'].index(intent.lower())]})</li>" for intent, percent in result.get('intentionality_breakdown', {}).items() if percent > 0])}
                        </ul>
                        <br>
                        <div style="background: #374151; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <strong>💡 Tip:</strong> Enable "Campaign Relevancy Analysis" in the sidebar to get a comprehensive score that includes how well this content fits your specific campaign objectives.
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<h2 class="section-header">📊 Performance Metrics</h2>', unsafe_allow_html=True)

        analysis_metadata = result.get("analysis_metadata", {})
        intentionality_score = calculate_intentionality_score(result)
        keyword_count = len(result.get("primary_keywords", [])) + len(result.get("secondary_keywords", []))
        audience_complexity = len(result.get("audience_profile", {}).get("type", []))
        campaign_score = campaign_relevancy.get('overall_relevancy_score', 0) if st.session_state.campaign_analysis and campaign_relevancy else None

        # Dynamic column layout based on whether campaign analysis is enabled
        if st.session_state.campaign_analysis and campaign_score is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Article Intent</div>
                        <div class="metric-value">{intentionality_score}/100</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Campaign Relevancy</div>
                        <div class="metric-value">{campaign_score}/100</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Keyword Count</div>
                        <div class="metric-value">{keyword_count}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Audience Segments</div>
                        <div class="metric-value">{audience_complexity}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Show only 3 columns when campaign analysis is disabled
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Intention Score</div>
                        <div class="metric-value">{intentionality_score}/100</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Keyword Count</div>
                        <div class="metric-value">{keyword_count}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Audience Segments</div>
                        <div class="metric-value">{audience_complexity}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    # TAB 2: ANALYTICS
    with tabs[1]:
        st.markdown('<h2 class="section-header">📈 Audience Analytics </h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age_chart = create_age_chart(demographics)
            if age_chart:
                st.plotly_chart(age_chart, use_container_width=True)
        
        with col2:
            gender_chart = create_gender_chart(demographics)
            if gender_chart:
                st.plotly_chart(gender_chart, use_container_width=True)
        
        with col3:
            intentionality_data = result.get('intentionality_breakdown', {})
            if intentionality_data:
                intent_chart = create_intentionality_chart(intentionality_data)
                if intent_chart:
                    st.plotly_chart(intent_chart, use_container_width=True)
        st.markdown('<h2 class="section-header">👤 Audience Profile</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            audience_types = result.get('audience_profile', {}).get('type', ['Unknown'])
            audience_text = ', '.join(audience_types) if isinstance(audience_types, list) else str(audience_types)
            
            regions = demographics.get('region', ['Unknown'])
            region_text = ', '.join(regions) if isinstance(regions, list) else str(regions)
            
            st.markdown(f"""
                <div class="content-card">
                    <div class="card-title">Demographics</div>
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.25rem;">Audience Type</div>
                        <div style="color: #E4E4E4; font-weight: 500;">{audience_text}</div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.25rem;">Region</div>
                        <div style="color: #E4E4E4; font-weight: 500;">{region_text}</div>
                    </div>
                    <div>
                        <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.25rem;">Gender</div>
                        <div style="color: #E4E4E4; font-weight: 500;">{demographics.get('gender', 'Unknown')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            profession = demographics.get('profession', 'Unknown')
            intent_signal = result.get('audience_profile', {}).get('intent_signal', 'No signal detected')
            
            st.markdown(f"""
                <div class="content-card">
                    <div class="card-title">Profile Details</div>
                    <div style="margin-bottom: 1rem;">
                        <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.25rem;">Profession</div>
                        <div style="color: #E4E4E4; font-weight: 500;">{profession}</div>
                    </div>
                    <div>
                        <div style="color: #9CA3AF; font-size: 0.875rem; margin-bottom: 0.25rem;">Intent Signal</div>
                        <div style="color: #E4E4E4; font-weight: 500; line-height: 1.5;">{intent_signal}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
         # Interest Groups
        interest_groups = result.get('audience_profile', {}).get('interest_groups', [])
        if interest_groups:
            st.markdown('<h3 class="section-header">👥 Interest Groups</h3>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="content-card">
                    <div class="card-title">Interest Categories</div>
                    <div style="margin-top: 1rem;">
                        {''.join([f'<span class="tag tag-secondary">{group}</span>' for group in interest_groups])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: CAMPAIGN (only if campaign analysis is enabled and data exists)
    tab_index = 2
    if st.session_state.campaign_analysis and campaign_relevancy:
        with tabs[tab_index]:
            st.markdown('<h2 class="section-header">🎯 Campaign Relevancy Analysis</h2>', unsafe_allow_html=True)
            
            overall_score = campaign_relevancy.get('overall_relevancy_score', 0)
            relevancy_level = campaign_relevancy.get('relevancy_level', 'unknown')
            recommendation = campaign_relevancy.get('recommendation', 'consider')
            
            # Campaign Summary Card
            recommendation_emoji = {
                'highly_recommend': '🚀',
                'recommend': '✅', 
                'consider': '⚠️',
                'avoid': '❌'
            }.get(recommendation, '🤔')
            
            st.markdown(f"""
                <div class="content-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <div>
                            <h3 style="color: #f7c3dc; margin: 0; font-size: 1.25rem;">Campaign Relevancy Assessment</h3>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{recommendation_emoji}</div>
                            <div style="color: {'#10B981' if overall_score >= 80 else '#F59E0B' if overall_score >= 60 else '#EF4444'}; font-weight: 700; font-size: 1.5rem;">
                                {overall_score}/100
                            </div>
                        </div>
                    </div>
                    <div style="color: #D1D5DB; font-size: 1rem; margin-bottom: 0.5rem;">
                        <strong>Recommendation:</strong> {recommendation.replace('_', ' ').title()}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Campaign Metrics Grid
            col1, col2, col3 = st.columns(3)

            with col1:
                strengths = campaign_relevancy.get('content_strengths_for_campaign', [])
                if strengths:
                    st.markdown(f"""
                        <div class="content-card">
                            <div class="card-title">✅ Content Strengths</div>
                            <ul style="color: #D1D5DB; line-height: 1.7; margin: 0; padding-left: 1.5rem;">
                                {''.join([f'<li>{strength}</li>' for strength in strengths])}
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="content-card">
                            <div class="card-title">✅ Content Strengths</div>
                            <p style="color: #9CA3AF; font-style: italic;">No matching content for the campaign definition</p>
                        </div>
                    """, unsafe_allow_html=True)

            with col2:
                intent_score = campaign_relevancy.get('intent_alignment_score', 0)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Intent Match</div>
                        <div class="metric-value">{intent_score}%</div>
                        <div class="metric-subtitle">User intent alignment</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                vertical_score = campaign_relevancy.get('vertical_alignment_score', 0)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Vertical Match</div>
                        <div class="metric-value">{vertical_score}%</div>
                        <div class="metric-subtitle">Industry alignment</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Performance Summary for campaign
            performance_summary = result.get('performance_summary', {})
            if performance_summary:
                st.markdown('<h3 class="section-header">🎯 Performance Summary</h3>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="summary-card">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                            <div>
                                <div class="metric-title" style="font-size: 0.875rem; margin-bottom: 0.25rem;">Article Intent</div>
                                <div class="metric-value" >{performance_summary.get('content_intent', 'Unknown').title()}</div>
                            </div>
                            <div>
                                <div class="metric-title" style=" font-size: 0.875rem; margin-bottom: 0.25rem;">Campaign Suitability</div>
                                <div class="metric-value" >{performance_summary.get('campaign_suitability', 'Unknown').title()}</div>
                            </div>
                            <div>
                                <div class="metric-title" style="font-size: 0.875rem; margin-bottom: 0.25rem;">Overall Relevancy</div>
                                <div class="metric-value" >{performance_summary.get('overall_relevancy', 'Unknown').title()}</div>
                            </div>
                            <div>
                                <div class="metric-title" style="margin-bottom: 0.25rem;">Final Recommendation</div>
                                <div class="metric-value" style="color: {'#10B981' if 'recommend' in performance_summary.get('recommendation', '') else '#F59E0B'}; font-weight: 600;">
                                    {performance_summary.get('recommendation', 'Unknown').replace('_', ' ').title()}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        tab_index += 1
    
    # TAB: KEYWORDS
    with tabs[tab_index]:
        st.markdown('<h2 class="section-header">🔑 Keywords</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            primary_keywords = result.get('primary_keywords', [])
            if primary_keywords:
                st.markdown(f"""
                    <div class="content-card">
                        <div class="card-title">Primary Keywords</div>
                        <div style="margin-top: 1rem;">
                            {''.join([f'<span class="tag">{kw}</span>' for kw in primary_keywords])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            secondary_keywords = result.get('secondary_keywords', [])
            if secondary_keywords:
                st.markdown(f"""
                    <div class="content-card">
                        <div class="card-title">Secondary Keywords</div>
                        <div style="margin-top: 1rem;">
                            {''.join([f'<span class="tag tag-secondary">{kw}</span>' for kw in secondary_keywords])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col3:
            # Keyword Distribution Chart
            if primary_keywords or secondary_keywords:
                keyword_chart = create_keyword_chart(primary_keywords, secondary_keywords)
                if keyword_chart:
                    st.plotly_chart(keyword_chart, use_container_width=True)
        
        # Matching Keywords (only show if campaign analysis was enabled)
        if st.session_state.campaign_analysis and campaign_relevancy:
            matching_keywords = campaign_relevancy.get('matching_keywords', [])
            if matching_keywords:
                st.markdown(f"""
                    <div class="content-card">
                        <div class="card-title">🎯 Campaign Keyword Matches</div>
                        <div style="margin-top: 1rem;">
                            {''.join([f'<span class="tag" style="background: #10B981 !important; color: #FFFFFF !important;">{kw}</span>' for kw in matching_keywords])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="content-card">
                        <div class="card-title">🎯 Campaign Keyword Matches</div>
                        <div style="margin-top: 1rem; color: #9CA3AF; font-style: italic;">
                            No matching keywords found between content and campaign
                        </div>
                    </div>
                """, unsafe_allow_html=True)


# Footer
footer_message = "Content Intelligence with Optional Campaign Analysis" if st.session_state.campaign_analysis else "Content Intelligence Analysis"
st.markdown(f"""
    <div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #6B7280; border-top: 1px solid #374151;">
        <p style="font-family: 'Inter', sans-serif; font-size: 0.875rem;">
            🎯 {footer_message} - Powered by Liz - Contextual Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)