import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import json
import re

st.set_page_config(page_title="ChartVision.ai", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #0B0E11; color: #EAECEF; }
        .stButton>button { width: 100%; background-color: #10B981 !important; color: white !important; font-weight: bold; }
        .emerald-text { color: #10B981; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>ChartVision<span class='emerald-text'>.ai</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Automate Your Chart Analysis with AI</p>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Choose Chart Image:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Chart', use_container_width=True)

    if st.button("Upload & Analyze Chart 🚀"):
        with st.spinner('AI analyzing chart... please wait.'):
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
                
                # JSON Clean up
                clean_text = re.sub(r'```json|```', '', response.text).strip()
                data = json.loads(clean_text)
                
                st.success("Analysis Completed!")
                st.json(data) # ප්‍රතිඵල පෙන්වනවා
                
            except Exception as e:
                st.error(f"Analysis Failed: {str(e)}")
                st.warning("Please try again with a clearer image.")