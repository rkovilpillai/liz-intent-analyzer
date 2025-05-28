## Contextual Article Analyzer - Updated Colors Only

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="🔮 Contextual Article Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Updated styling with your custom colors
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
    
    .metric-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #6B7280;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    .content-card {
        background: #272b39bf;
        border: 1px solid #2A2A3E;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
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
    
    .confidence-high {
        background: #10B981;
        color: #FFFFFF;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .confidence-medium {
        background: #F59E0B;
        color: #FFFFFF;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .confidence-low {
        background: #EF4444;
        color: #FFFFFF;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .chart-container {
        background: #272b39bf;
        border: 1px solid #2A2A3E;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 400px;
        position: relative;
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
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-item {
        background: #272b39bf;
        border: 1px solid #2A2A3E;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stat-item:hover {
        border-color: #8B5CF6;
        transform: translateY(-2px);
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #CD574C;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
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
    
    .stExpander {
        background: #272b39bf !important;
        border: 1px solid #2A2A3E !important;
        border-radius: 12px !important;
    }
    
    .stExpander > div > div {
        background: #272b39bf !important;
        color: #E4E4E4 !important;
    }
    
    /* Hide Streamlit branding */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Function to create age distribution chart with multiple colors
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
        textfont=dict(color="#FFFFFF", size=12, family="Inter", weight="bold")
    ))
    
    fig.update_layout(
        title="Real-Time Age Distribution",
        title_font=dict(color="#f7c3dc", family="Inter", size=16, weight=600),
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

# Function to create gender distribution chart with custom colors
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
        title_font=dict(color="#f7c3dc", family="Inter", size=16, weight=600),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#9CA3AF", family="Inter"),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

# Function to create intentionality breakdown chart
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
        title_font=dict(color="#f7c3dc", family="Inter", size=16, weight=600),
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

# Function to create keyword importance chart
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
        title_font=dict(color="#f7c3dc", family="Inter", size=16, weight=600),
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

# Function to calculate performance metrics
def calculate_intent_accuracy(result):
    intention = result.get('intention', {})
    confidence = intention.get('confidence', 'Low')
    confidence_accuracy = {'High': 85, 'Medium': 70, 'Low': 50}
    accuracy = confidence_accuracy.get(confidence, 50)
    
    intentionality = result.get('intentionality_breakdown', {})
    if intentionality and any(val > 0 for val in intentionality.values()):
        accuracy += 10
    
    return min(accuracy, 99)

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
st.markdown('<p class="subtitle">AI-powered content intelligence and audience insights</p>', unsafe_allow_html=True)

# Input section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    url = st.text_input("Article URL", placeholder="Enter article URL to analyze...", label_visibility="collapsed")

# N8N webhook URL
n8n_webhook_url = "https://rajkpillai.app.n8n.cloud/webhook/contextual-engine"

if url:
    with st.spinner("Analyzing content..."):
        try:
            response = requests.get(f"{n8n_webhook_url}?url={url}")
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    if isinstance(result_data, list):
                        result = result_data[0]
                    else:
                        result = result_data
                    
                    # Overview metrics
                    st.markdown('<h2 class="section-header">Overview</h2>', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
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
                    
                    # Analytics Charts
                    st.markdown('<h2 class="section-header">Analytics</h2>', unsafe_allow_html=True)
                    
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
                    
                    # Content Summary
                    st.markdown('<h2 class="section-header">Summary</h2>', unsafe_allow_html=True)
                    
                    summary = result.get('summary_rationale', 'No summary available')
                    st.markdown(f"""
                        <div class="summary-card">
                            <div class="summary-text">{summary}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Keywords
                    st.markdown('<h2 class="section-header">Keywords</h2>', unsafe_allow_html=True)
                    
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
                        # Keyword Distribution Chart
                        if primary_keywords or secondary_keywords:
                            keyword_chart = create_keyword_chart(primary_keywords, secondary_keywords)
                            if keyword_chart:
                                st.plotly_chart(keyword_chart, use_container_width=True)
                    
                    # Interest Groups
                    interest_groups = result.get('audience_profile', {}).get('interest_groups', [])
                    if interest_groups:
                        st.markdown('<h2 class="section-header">Interest Groups</h2>', unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class="content-card">
                                <div class="card-title">Interest Categories</div>
                                <div>
                                    {''.join([f'<span class="tag tag-secondary">{group}</span>' for group in interest_groups])}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Performance Metrics
                    st.markdown('<h2 class="section-header">Performance Metrics</h2>', unsafe_allow_html=True)
                    
                    intent_accuracy = calculate_intent_accuracy(result)
                    content_score = calculate_content_score(result)
                    keyword_count = len(primary_keywords) + len(secondary_keywords)
                    audience_complexity = len(result.get('audience_profile', {}).get('type', []))
                    
                    st.markdown(f"""
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-label">Intent Accuracy</div>
                                <div class="stat-value">{intent_accuracy}%</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Keyword Count</div>
                                <div class="stat-value">{keyword_count}</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Audience Segments</div>
                                <div class="stat-value">{audience_complexity}</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-label">Content Score</div>
                                <div class="stat-value">{content_score}/100</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Audience Profile
                    st.markdown('<h2 class="section-header">Audience Profile</h2>', unsafe_allow_html=True)
                    
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
                    with st.expander("Raw Data", expanded=False):
                        st.json(result)
                        
                except Exception as e:
                    st.error(f"Error parsing response: {e}")
            else:
                st.error(f"API request failed. Status code: {response.status_code}")
                
        except Exception as e:
            st.error(f"Request failed: {e}")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #6B7280; border-top: 1px solid #374151;">
        <p style="font-family: 'Inter', sans-serif; font-size: 0.875rem;">
            Powered by Contextual AI Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)