import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Quantum Zeus 1.0",
    page_icon="⚡️",
    layout="centered",
)

# Get and validate API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Set up Gemini model
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro")
except Exception as e:
    st.error(f"Error initializing Gemini API: {e}")
    st.stop()

# Role mapping for display
def translate_role(role):
    return "assistant" if role == "model" else role

# Initialize session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("🤖 Quantum Zeus 1.0 (Powered by Google Gemini)")

# Chat history display
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text if message.parts else "(empty)")

# Chat input
user_prompt = st.chat_input("Ask Zeus anything...")
if user_prompt:
    try:
        st.chat_message("user").markdown(user_prompt)
        response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Chat error: {e}")
