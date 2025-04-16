import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from lambeq import BobcatParser
import torch

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Quantum Zeus 1.0",
    page_icon="⚡️",
    layout="centered",
)

# Get and validate API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Error: GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Set up Google Gemini AI model
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
except Exception as e:
    st.error(f"Error initializing Gemini API: {str(e)}")
    st.stop()

# Quantum NLP: Example of integrating quantum logic using Lambeq (only symbolic here)
def quantum_nlp_process(input_text):
    # This function can be extended to integrate quantum NLP processing
    try:
        # Placeholder for actual quantum NLP processing
        parser = BobcatParser()
        return parser.parse(input_text)  # Simulate quantum NLP processing
    except Exception as e:
        return f"Quantum NLP Error: {str(e)}"

# Role mapping for display
def translate_role(role):
    return "assistant" if role == "model" else role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title of the page
st.title("🤖 Quantum Zeus 1.0 (Powered by Google Gemini)")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text if message.parts else "(empty)")

# Input from the user
user_prompt = st.chat_input("Ask Zeus anything...")
if user_prompt:
    try:
        # Display user input
        st.chat_message("user").markdown(user_prompt)
        
        # Here, you can optionally process the input with Quantum NLP
        processed_prompt = quantum_nlp_process(user_prompt)

        # Send the user input (or processed input) to Gemini model
        response = st.session_state.chat_session.send_message(processed_prompt)
        
        # Display assistant's response
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error processing chat: {str(e)}")
