# Contextual Article Analyzer

AI-powered content intelligence and audience insights dashboard built with Streamlit.

## Features

- 🎯 **Intent Analysis** - Detects primary and secondary content intentions
- 📊 **Audience Demographics** - Real-time age and gender distribution
- 🔑 **Keyword Intelligence** - Primary and secondary keyword identification
- 📈 **Performance Metrics** - Content scoring and intent accuracy
- 🎨 **Interactive Visualizations** - Charts and graphs for data insights

## Technology Stack

- **Frontend**: Streamlit
- **Charts**: Plotly
- **API Integration**: N8N Webhook
- **Styling**: Custom CSS with modern dark theme

## Live Demo

🚀 [View Live App](https://your-app-name.streamlit.app)

## How to Use

1. Enter an article URL in the input field
2. Wait for AI analysis to complete
3. Explore the interactive dashboard with:
   - Content overview and metrics
   - Age and gender distribution charts
   - Intent breakdown analysis
   - Keyword distribution
   - Audience profiling

## Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/contextual-analyzer.git
cd contextual-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deployment

This app is deployed on Streamlit Cloud and automatically updates from the main branch.

## API Integration

The app connects to an N8N workflow for content analysis. The webhook processes article URLs and returns:

- Content categorization
- Audience demographics
- Intent classification
- Keyword extraction
- Performance scoring

---

*Powered by Contextual AI Intelligence*