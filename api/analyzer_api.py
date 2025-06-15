import streamlit as st
import requests
from urllib.parse import urlencode
from config.settings import N8N_WEBHOOK_URL_BASIC, N8N_WEBHOOK_URL_CAMPAIGN

def analyze_content(processed_url, campaign_definition="", vertical=""):
    """Analyze content using the API"""
    # Start analysis
    st.session_state.analysis_complete = False
    
    # Show appropriate spinner message
    spinner_message = ("🔮 Liz - Analyzing content and campaign relevancy..." 
                      if st.session_state.campaign_analysis 
                      else "🔮 Liz - Analyzing article content...")
    
    with st.spinner(spinner_message):
        try:
            # Choose API endpoint and payload based on campaign analysis toggle
            if st.session_state.campaign_analysis:
                # Campaign analysis enabled
                api_url = N8N_WEBHOOK_URL_CAMPAIGN
                params = {
                    'url': processed_url,
                    'campaign_definition': campaign_definition,
                    'vertical': vertical
                }
            else:
                # Basic analysis only
                api_url = N8N_WEBHOOK_URL_BASIC
                params = {
                    'url': processed_url
                }
            
            # Encode parameters and make request
            encoded_params = urlencode(params)
            full_api_url = f"{api_url}?{encoded_params}"
            
            # Make API call
            response = requests.get(full_api_url, timeout=30)
            
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    
                    # Handle error responses
                    if isinstance(result_data, list) and len(result_data) > 0 and "error" in result_data[0]:
                        result = result_data[0]
                        st.error(f"⚠️ {result.get('message', 'An error occurred.')}")
                        if result.get("suggestions"):
                            for suggestion in result.get("suggestions", []):
                                st.info(f"💡 {suggestion}")
                    else:
                        # Successfully got analysis results
                        if isinstance(result_data, list):
                            result = result_data[0]
                        else:
                            result = result_data
                        
                        # Store results in session state
                        st.session_state.analysis_results = result
                        st.session_state.analysis_complete = True
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error parsing response: {e}")
            else:
                st.error(f"API request failed. Status code: {response.status_code}")
                st.write("Response:", response.text[:500])

        except Exception as e:
            st.error(f"Request failed: {e}")