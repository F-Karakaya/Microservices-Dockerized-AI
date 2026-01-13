import streamlit as st
import requests
import os
import json

# Configuration
# API Gateway URL should be accessible from the container or host
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:5000/api/inference")

st.set_page_config(
    page_title="AI Service Demo",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Microservices AI Demo")
st.markdown("""
This is a simple frontend service interacting with the backend API Gateway.
All requests are routed through the Gateway to the AI Service.
""")

st.subheader("Sentiment Analysis")

# Input form
with st.form("inference_form"):
    text_input = st.text_area("Enter text to analyze", "I love building scalable microservices with Docker and Kubernetes!")
    submitted = st.form_submit_button("Analyze Sentiment")

if submitted:
    if not text_input:
        st.warning("Please enter some text.")
    else:
        with st.spinner("Requesting inference from API Gateway..."):
            try:
                # Prepare payload
                payload = {"text": text_input}
                
                # Send request to API Gateway
                response = requests.post(API_GATEWAY_URL, json=payload)
                
                # Display results
                if response.status_code == 200:
                    result = response.json()
                    st.success("Inference Successful!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Sentiment", result.get("sentiment", "Unknown"))
                    with col2:
                        confidence = result.get("confidence", 0.0)
                        st.metric("Confidence", f"{confidence:.4f}")
                        
                    st.json(result)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error(f"Failed to connect to API Gateway at {API_GATEWAY_URL}. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("### Service Status")
st.info(f"Connected to Gateway: `{API_GATEWAY_URL}`")
