import streamlit as st
from components.charts import create_age_chart, create_gender_chart, create_intentionality_chart, create_keyword_chart
from components.metrics import calculate_intentionality_score, get_intentionality_grade, calculate_final_intention_score, get_final_intention_grade

def render_video_waiting_state():
    """Render the enhanced video waiting state from your current app"""
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

def render_overview_tab(result):
    """Render the Overview tab content"""
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
        campaign_relevancy = result.get('campaign_relevancy', {})
        campaign_score = campaign_relevancy.get('overall_relevancy_score', 0) if st.session_state.campaign_analysis and campaign_relevancy else None
        
        if st.session_state.campaign_analysis and campaign_score is not None:
            # Final Intentionality Score
            final_intentionality_score, score_type = calculate_final_intention_score(result, campaign_relevancy)
            final_grade, final_grade_desc = get_final_intention_grade(final_intentionality_score, score_type)
            
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
    
    # Dynamic Intentionality Score Explanation
    campaign_relevancy = result.get('campaign_relevancy', {})
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

    # Performance Metrics
    st.markdown('<h2 class="section-header">📊 Performance Metrics</h2>', unsafe_allow_html=True)

    intentionality_score = calculate_intentionality_score(result)
    keyword_count = len(result.get("primary_keywords", [])) + len(result.get("secondary_keywords", []))
    audience_complexity = len(result.get("audience_profile", {}).get("type", []))

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
                    <div class="metric-title">Article Intent</div>
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

def render_audience_tab(result):
    """Render the Audience & Insights tab content"""
    st.markdown('<h2 class="section-header">📈 Audience Analytics</h2>', unsafe_allow_html=True)
    
    demographics = result.get('audience_profile', {}).get('demographics', {})
    
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

def render_campaign_tab(result):
    """Render the Campaign tab content"""
    st.markdown('<h2 class="section-header">🎯 Campaign Relevancy Analysis</h2>', unsafe_allow_html=True)
    
    campaign_relevancy = result.get('campaign_relevancy', {})
    
    overall_score = campaign_relevancy.get('overall_relevancy_score', 0)
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
                        <div class="metric-value">{performance_summary.get('content_intent', 'Unknown').title()}</div>
                    </div>
                    <div>
                        <div class="metric-title" style="font-size: 0.875rem; margin-bottom: 0.25rem;">Campaign Suitability</div>
                        <div class="metric-value">{performance_summary.get('campaign_suitability', 'Unknown').title()}</div>
                    </div>
                    <div>
                        <div class="metric-title" style="font-size: 0.875rem; margin-bottom: 0.25rem;">Overall Relevancy</div>
                        <div class="metric-value">{performance_summary.get('overall_relevancy', 'Unknown').title()}</div>
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

def render_keywords_tab(result):
    """Render the Keywords tab content"""
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
    campaign_relevancy = result.get('campaign_relevancy', {})
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

def render_main_content():
    """Main function to render the complete main content area with tabs"""
    
    # Results Container
    if not st.session_state.analysis_complete or st.session_state.analysis_results is None:
        # Video waiting state
        render_video_waiting_state()
    else:
        # Display results with tabs
        result = st.session_state.analysis_results
        
        # Create dynamic tab list based on campaign analysis toggle
        tab_list = ["📊 Overview", "👤 Audience 📈 Insights", "🔑 Keywords"]
        
        # Add campaign tab if campaign analysis is enabled and data exists
        campaign_relevancy = result.get('campaign_relevancy', {})
        if st.session_state.campaign_analysis and campaign_relevancy:
            tab_list.insert(2, "🎯 Campaign")
        
        # Create tabs
        tabs = st.tabs(tab_list)
        
        # TAB 1: OVERVIEW
        with tabs[0]:
            render_overview_tab(result)
        
        # TAB 2: AUDIENCE & INSIGHTS
        with tabs[1]:
            render_audience_tab(result)
        
        # TAB 3: CAMPAIGN (only if campaign analysis is enabled and data exists)
        tab_index = 2
        if st.session_state.campaign_analysis and campaign_relevancy:
            with tabs[tab_index]:
                render_campaign_tab(result)
            tab_index += 1
        
        # TAB: KEYWORDS
        with tabs[tab_index]:
            render_keywords_tab(result)