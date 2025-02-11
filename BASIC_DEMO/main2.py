import vertexai
import streamlit as st
import os
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set authentication credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Authenticate with Vertex AI using credentials from the JSON file
vertexai.init()

# Load the model
model = GenerativeModel("gemini-1.0-pro")

def user_interfaces():
    st.set_page_config(page_title="VertexAI demo")
    st.header("VertexAI Local Demo")

    user_question = st.text_input("Ask me anything....")

    if user_question: 
        response = model.generate_content(user_question, stream=True)

        for res in response:
            st.write(res.text)

if __name__ == "__main__":
    user_interfaces()
