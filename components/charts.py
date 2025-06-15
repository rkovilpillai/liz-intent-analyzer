import plotly.graph_objects as go
import plotly.express as px

def create_age_chart(demographics):
    """Create age distribution chart"""
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
    """Create gender distribution pie chart"""
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
    """Create intentionality radar chart"""
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
    """Create keyword distribution pie chart"""
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