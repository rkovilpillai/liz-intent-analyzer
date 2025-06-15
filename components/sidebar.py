import plotly.graph_objects as go
import plotly.express as px
# components/sidebar.py

import streamlit as st
from config.constants import IAB_TIER1_CATEGORIES
from api.validators import is_valid_url
from api.analyzer_api import analyze_content
from auth.google_auth import logout_user

def render_url_input_section():
    """Render the URL input section"""
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">📄 Article URL</div>
        </div>
    """, unsafe_allow_html=True)
    
    return st.text_input(
        "Enter article URL",
        placeholder="https://example.com/article",
        help="Enter the full URL of the article you want to analyze",
        label_visibility="collapsed"
    )

def render_campaign_toggle_section():
    """Render the campaign analysis toggle section"""
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">🎯 Analysis Options</div>
        </div>
    """, unsafe_allow_html=True)
    
    campaign_toggle = st.checkbox(
        "Enable Campaign Relevancy Analysis",
        value=st.session_state.campaign_analysis,
        help="Turn on to analyze how well this content fits your specific campaign objectives"
    )
    
    # Update session state immediately when toggle changes
    if campaign_toggle != st.session_state.campaign_analysis:
        st.session_state.campaign_analysis = campaign_toggle
        st.rerun()
    
    return campaign_toggle

def render_campaign_fields():
    """Render campaign definition and vertical selection fields"""
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
    
    return campaign_definition, vertical

def render_analyze_button(url, campaign_definition, vertical):
    """Render the analyze button with appropriate text and state"""
    if st.session_state.campaign_analysis:
        button_text = "🔍 Analyze Article & Campaign Relevancy"
        button_disabled = not url or not campaign_definition or not vertical
    else:
        button_text = "🔍 Analyze Article Content"
        button_disabled = not url
    
    if st.button(button_text, disabled=button_disabled, use_container_width=True):
        is_valid, processed_url = is_valid_url(url)
        if not is_valid:
            st.error(processed_url)
        else:
            analyze_content(processed_url, campaign_definition, vertical)

def render_help_section():
    """Render the help/tips section"""
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

def render_logout_section():
    """Render the logout section at the bottom of sidebar"""
    if st.session_state.credentials:
        st.markdown("""
            <div class="logout-section">
                <div class="user-info">✅ Successfully authenticated with Google</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            logout_user()

def render_sidebar():
    """Main function to render the complete sidebar"""
    with st.sidebar:
        # Header
        st.markdown('<h2 class="sidebar-header">🔮 Article Analyzer</h2>', unsafe_allow_html=True)
        
        # URL Input Section
        url = render_url_input_section()
        
        # Campaign Toggle Section
        campaign_toggle = render_campaign_toggle_section()
        
        # Campaign Fields (appears when toggle is enabled)
        campaign_definition, vertical = render_campaign_fields()
        
        # Analyze Button
        render_analyze_button(url, campaign_definition, vertical)
        
        # Help Section
        render_help_section()
        
        # Logout Section (at the bottom)
        render_logout_section()

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
    # Similar structure for gender chart
    pass

def create_intentionality_chart(intentionality_data):
    # Similar structure for intentionality chart
    pass

def create_keyword_chart(primary_kw, secondary_kw):
    # Similar structure for keyword chart
    pass