
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound  # Import the NotFound exception.

load_dotenv()  # Load environment variables from .env file.

# Configure Google API key.
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("Google API key is missing. Please set it in your .env file.")
    st.stop()

# Try to configure the generative AI model.
try:
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize generative model.
except NotFound:
    st.error("The specified Google model was not found. Please check the model name or your API configuration.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.stop()

# Function to get Gemini response.
def get_gemini_response(input, image):
    if input:
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Streamlit app initialization.
st.set_page_config(page_title="Iridium AI")

# Load and display Iridium logo.
logo_path = "Images/IridiumAILogo.png"
iridium_logo = Image.open(logo_path)
st.image(iridium_logo, use_column_width=False)

st.header("Iridium AI: AI-Powered Image Analysis")

input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit_button = st.button("Analyze Image")

if submit_button:
    if not uploaded_file:
        st.warning("Please upload an image.")
    else:
        response = get_gemini_response(input_prompt, image)
        st.subheader("Response")
        st.write(response)
























