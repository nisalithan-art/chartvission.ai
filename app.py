import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

st.set_page_config(page_title="ChartVision.ai", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #0B0E11; color: #EAECEF; }
        .stButton>button { width: 100%; background-color: #10B981 !important; color: white !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("ChartVision.ai")

genai.configure(api_key="AQ.Ab8RN6IGQCk63S_YennYCERWbaM6ei0JUdp5cmjTSmA4fXOekA")
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload chart image:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)

    if st.button("Analyze Chart 🚀"):
        with st.spinner('AI analyzing...'):
            try:
                prompt = """
                Analyze this trading chart. 
                Identify absolute max price, absolute min price, and 1-3 major support/resistance levels.
                Respond ONLY in valid JSON format:
                {
                    "price_max": 0.0,
                    "price_min": 0.0,
                    "support_levels": [],
                    "resistance_levels": []
                }
                """
                response = model.generate_content([prompt, img])
                clean_text = re.sub(r'```json|```', '', response.text).strip()
                data = json.loads(clean_text)
                st.success("Analysis Completed!")
                st.json(data)
            except Exception as e:
                st.error(f"Error: {e}")
               
