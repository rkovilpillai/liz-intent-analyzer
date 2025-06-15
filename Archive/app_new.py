## Contextual Article Analyzer - Step 1: Campaign Inputs

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
    initial_sidebar_state="collapsed"
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

# Your existing styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #181c2b;
        color: #E4E4E4;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #f7c3dc;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #9CA3AF;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #f7c3dc;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.01em;
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
    }
    
    .stButton > button:hover {
        background: #7C3AED !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Hide Streamlit branding */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
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
    confidence_scores = {'High': 40, 'Medium': 30, 'Low': 20}
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

# Header
st.markdown('<h1 class="main-header">Contextual Article Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">LIZ - powered content intelligence with campaign context</p>', unsafe_allow_html=True)

# Enhanced input section with campaign context
with st.form("analysis_form"):
    # URL Input
    st.markdown("### 📄 Article to Analyze")
    url = st.text_input("Article URL", placeholder="https://example.com/article", help="Enter the full URL of the article you want to analyze")
    
    # Campaign Context Section (Clean, minimal design)
    st.markdown("### 🎯 Campaign Context")
    col1, col2 = st.columns(2)
    
    with col1:
        campaign_definition = st.text_area(
            "Campaign Definition", 
            placeholder="e.g., Summer running shoes for marathon training targeting serious athletes aged 25-45",
            help="Describe your campaign objective, target audience, and key messaging",
            height=100
        )
    
    with col2:
        vertical = st.selectbox(
            "Target Vertical (IAB Tier 1)",
            options=[""] + IAB_TIER1_CATEGORIES,
            help="Select the primary industry/vertical for your campaign"
        )
    
    # Submit button
    st.markdown("### 🚀 Analysis")
    submitted = st.form_submit_button("🔍 Analyze Article & Campaign Relevancy", use_container_width=True)

# Simple API test (using your original working webhook)
n8n_webhook_url = "https://rajkpillai.app.n8n.cloud/webhook-test/contextual-engine-v2"

if submitted:
    # Validate inputs
    if not url:
        st.error("⚠️ Please enter an article URL")
        st.stop()
    
    if not campaign_definition:
        st.error("⚠️ Please provide a campaign definition")
        st.stop()
        
    if not vertical:
        st.error("⚠️ Please select a target vertical")
        st.stop()
    
    # Validate URL format
    is_valid, processed_url = is_valid_url(url)
    if not is_valid:
        display_error("invalid_url", processed_url)
        st.stop()
    
# Simple API test (using your working webhook)
n8n_webhook_url = "https://rajkpillai.app.n8n.cloud/webhook-test/contextual-engine-test"

if submitted:
    # Validate inputs
    if not url:
        st.error("⚠️ Please enter an article URL")
        st.stop()
    
    if not campaign_definition:
        st.error("⚠️ Please provide a campaign definition")
        st.stop()
        
    if not vertical:
        st.error("⚠️ Please select a target vertical")
        st.stop()
    
    # Validate URL format
    is_valid, processed_url = is_valid_url(url)
    if not is_valid:
        display_error("invalid_url", processed_url)
        st.stop()
    
    with st.spinner("🔮 LIZ is analyzing content and campaign relevancy..."):
        try:
            # Prepare parameters for URL encoding
            params = {
                'url': processed_url,
                'campaign_definition': campaign_definition,
                'vertical': vertical
            }
            
            # Build the complete URL with properly encoded parameters
            encoded_params = urlencode(params)
            api_url = f"{n8n_webhook_url}?{encoded_params}"
            
            # Make the GET request with all parameters
            response = requests.get(api_url, timeout=30)
            
            # If GET fails, try POST with JSON payload
            if response.status_code != 200:
                payload = {
                    "query": {
                        "url": processed_url,
                        "campaign_definition": campaign_definition,
                        "vertical": vertical
                    }
                }
                response = requests.post(n8n_webhook_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    
                    # Handle error responses
                    if isinstance(result_data, list) and len(result_data) > 0 and "error" in result_data[0]:
                        result = result_data[0]
                        display_error(
                            error_type=result.get("error_type", "general"),
                            message=result.get("message", "An error occurred."),
                            suggestions=result.get("suggestions", []),
                            technical_details=f"URL: {processed_url}\nCampaign: {campaign_definition}\nVertical: {vertical}"
                        )
                        st.stop()
                    
                    if isinstance(result_data, list):
                        result = result_data[0]
                    else:
                        result = result_data
                    
                    # 📊 CONTENT INTELLIGENCE FIRST (Original clean design)
                    st.markdown('<h2 class="section-header">📊 Content Intelligence</h2>', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        intention = result.get('intention', {})
                        primary_intent = intention.get('primary', 'Unknown')
                        confidence = intention.get('confidence', 'Unknown')
                        confidence_class = f"confidence-{confidence.lower()}" if confidence != 'Unknown' else "confidence-low"
                        
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Intent</div>
                                <div class="metric-value">{primary_intent.title()}</div>
                                <div class="metric-subtitle">
                                    <span class="{confidence_class}">{confidence}</span>
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
                                <div class="metric-title">Action Score</div>
                                <div class="metric-value" style="color: {score_color};">{intentionality_score}/100</div>
                                <div class="metric-subtitle">
                                    <span style="color: {score_color}; font-weight: 600;">{grade}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Analytics Charts (Clean original design)
                    st.markdown('<h2 class="section-header">📈 Analytics</h2>', unsafe_allow_html=True)
                    
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
                    
                    # 🎯 CAMPAIGN ANALYSIS SECTION (Clean, professional design)
                    st.markdown('<h2 class="section-header">🎯 Campaign Relevancy Analysis</h2>', unsafe_allow_html=True)
                    
                    campaign_relevancy = result.get('campaign_relevancy', {})
                    
                    if campaign_relevancy:
                        overall_score = campaign_relevancy.get('overall_relevancy_score', 0)
                        relevancy_level = campaign_relevancy.get('relevancy_level', 'unknown')
                        recommendation = campaign_relevancy.get('recommendation', 'consider')
                        
                        # Clean Campaign Summary Card
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
                                        <h3 style="color: #f7c3dc; margin: 0; font-size: 1.25rem;">Campaign Fit Assessment</h3>
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
                                <div style="color: #9CA3AF; font-size: 0.9rem;">
                                    Campaign: {campaign_definition}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Clean Campaign Metrics Grid
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            keyword_score = campaign_relevancy.get('keyword_alignment_score', 0)
                            st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-title">Keyword Match</div>
                                    <div class="metric-value">{keyword_score}%</div>
                                    <div class="metric-subtitle">Content keywords alignment</div>
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
                        
                        with col4:
                            audience_score = campaign_relevancy.get('audience_match_score', 0)
                            st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-title">Audience Match</div>
                                    <div class="metric-value">{audience_score}%</div>
                                    <div class="metric-subtitle">Target audience fit</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Campaign Insights (Clean layout)
                        col1, col2 = st.columns(2)
                        
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
                        
                        with col2:
                            gaps = campaign_relevancy.get('content_gaps_for_campaign', [])
                            if gaps:
                                st.markdown(f"""
                                    <div class="content-card">
                                        <div class="card-title">🔧 Areas for Improvement</div>
                                        <ul style="color: #D1D5DB; line-height: 1.7; margin: 0; padding-left: 1.5rem;">
                                            {''.join([f'<li>{gap}</li>' for gap in gaps])}
                                        </ul>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        # Optimization Suggestions
                        suggestions = campaign_relevancy.get('optimization_suggestions', [])
                        if suggestions:
                            st.markdown(f"""
                                <div class="content-card">
                                    <div class="card-title">💡 Optimization Recommendations</div>
                                    <ul style="color: #D1D5DB; line-height: 1.7; margin: 0; padding-left: 1.5rem;">
                                        {''.join([f'<li>{suggestion}</li>' for suggestion in suggestions])}
                                    </ul>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Content Summary (Clean design)
                    st.markdown('<h2 class="section-header">📝 Summary</h2>', unsafe_allow_html=True)
                    
                    summary = result.get('summary_rationale', 'No summary available')
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-text">{summary}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Keywords (Professional pill design)
                    st.markdown('<h2 class="section-header">🔑 Keywords</h2>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
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
                    
                    # Matching Keywords (if available)
                    if campaign_relevancy:
                        matching_keywords = campaign_relevancy.get('matching_keywords', [])
                        if matching_keywords:
                            st.markdown(f"""
                                <div class="content-card">
                                    <div class="card-title">🎯 Campaign Keyword Matches</div>
                                    <div style="margin-top: 1rem;">
                                        {''.join([f'<span class="tag" style="background: #10B981;">{kw}</span>' for kw in matching_keywords])}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Interest Groups (Clean design)
                    interest_groups = result.get('audience_profile', {}).get('interest_groups', [])
                    if interest_groups:
                        st.markdown('<h2 class="section-header">👥 Interest Groups</h2>', unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class="content-card">
                                <div class="card-title">Target Interest Categories</div>
                                <div style="margin-top: 1rem;">
                                    {''.join([f'<span class="tag tag-secondary">{group}</span>' for group in interest_groups])}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Performance Metrics (Clean grid)
                    st.markdown('<h2 class="section-header">📊 Performance Metrics</h2>', unsafe_allow_html=True)

                    analysis_metadata = result.get("analysis_metadata", {})
                    intent_accuracy = calculate_intent_accuracy(result)
                    intentionality_score = calculate_intentionality_score(result)
                    keyword_count = len(result.get("primary_keywords", [])) + len(result.get("secondary_keywords", []))
                    audience_complexity = len(result.get("audience_profile", {}).get("type", []))
                    campaign_score = campaign_relevancy.get('overall_relevancy_score', 0) if campaign_relevancy else 0

                    st.markdown(f"""
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-label">Intent Accuracy</div>
                                <div class="stat-value">{intent_accuracy}%</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Action Score</div>
                                <div class="stat-value">{intentionality_score}/100</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Campaign Fit</div>
                                <div class="stat-value">{campaign_score}/100</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Keywords</div>
                                <div class="stat-value">{keyword_count}</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Audience Segments</div>
                                <div class="stat-value">{audience_complexity}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Audience Profile (Clean layout)
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
                                    <div class="stat-label">Audience Type</div>
                                    <div style="color: #E4E4E4; font-weight: 500;">{audience_text}</div>
                                </div>
                                <div style="margin-bottom: 1rem;">
                                    <div class="stat-label">Region</div>
                                    <div style="color: #E4E4E4; font-weight: 500;">{region_text}</div>
                                </div>
                                <div>
                                    <div class="stat-label">Gender</div>
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
                                    <div class="stat-label">Profession</div>
                                    <div style="color: #E4E4E4; font-weight: 500;">{profession}</div>
                                </div>
                                <div>
                                    <div class="stat-label">Intent Signal</div>
                                    <div style="color: #E4E4E4; font-weight: 500; line-height: 1.5;">{intent_signal}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Raw Data
                    with st.expander("Raw API Response", expanded=False):
                        st.json(result)
                    
                    with col5:
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
                                <div class="metric-title">Action Score</div>
                                <div class="metric-value" style="color: {score_color};">{intentionality_score}/100</div>
                                <div class="metric-subtitle">
                                    <span style="color: {score_color}; font-weight: 600;">{grade}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Analytics Charts
                    st.markdown('<h2 class="section-header">📈 Analytics</h2>', unsafe_allow_html=True)
                    
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
                    
                    # Summary
                    st.markdown('<h2 class="section-header">📝 Summary</h2>', unsafe_allow_html=True)
                    
                    summary = result.get('summary_rationale', 'No summary available')
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-text">{summary}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Keywords
                    st.markdown('<h2 class="section-header">🔑 Keywords</h2>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        primary_keywords = result.get('primary_keywords', [])
                        if primary_keywords:
                            st.markdown(f"""
                                <div class="content-card">
                                    <div class="card-title">Primary Keywords</div>
                                    <div>
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
                                    <div>
                                        {''.join([f'<span class="tag tag-secondary">{kw}</span>' for kw in secondary_keywords])}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with col3:
                        if primary_keywords or secondary_keywords:
                            keyword_chart = create_keyword_chart(primary_keywords, secondary_keywords)
                            if keyword_chart:
                                st.plotly_chart(keyword_chart, use_container_width=True)
                    
                    # Performance Summary
                    st.markdown('<h2 class="section-header">🎯 Performance Summary</h2>', unsafe_allow_html=True)
                    
                    performance_summary = result.get('performance_summary', {})
                    if performance_summary:
                        st.markdown(f"""
                            <div class="summary-card">
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                                    <div>
                                        <div class="stat-label">Content Intent</div>
                                        <div class="stat-value">{performance_summary.get('content_intent', 'Unknown').title()}</div>
                                    </div>
                                    <div>
                                        <div class="stat-label">Campaign Suitability</div>
                                        <div class="stat-value">{performance_summary.get('campaign_suitability', 'Unknown').title()}</div>
                                    </div>
                                    <div>
                                        <div class="stat-label">Overall Relevancy</div>
                                        <div class="stat-value">{performance_summary.get('overall_relevancy', 'Unknown').title()}</div>
                                    </div>
                                    <div>
                                        <div class="stat-label">Final Recommendation</div>
                                        <div class="stat-value" style="color: {'#10B981' if 'recommend' in performance_summary.get('recommendation', '') else '#F59E0B'};">
                                            {performance_summary.get('recommendation', 'Unknown').replace('_', ' ').title()}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Raw Data
                    with st.expander("Raw API Response", expanded=False):
                        st.json(result)
                        
                except Exception as e:
                    st.error(f"Error parsing response: {e}")
            else:
                st.error(f"API request failed. Status code: {response.status_code}")
                st.write("Response:", response.text)
                
        except Exception as e:
            st.error(f"Request failed: {e}")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #6B7280; border-top: 1px solid #374151;">
        <p style="font-family: 'Inter', sans-serif; font-size: 0.875rem;">
            🎯 Step 1: Campaign Context Integration - Powered by Contextual AI Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)