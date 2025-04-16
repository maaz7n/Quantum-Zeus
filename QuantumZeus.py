import os
import streamlit as st
import toml
from dotenv import load_dotenv
import google.generativeai as gen_ai
import pennylane as qml
import numpy as np

# Load environment variables from .env (if needed)
load_dotenv()

# Load config.toml
config_path = "/Users/mohammedmazin/Downloads/quantum_config.toml"

try:
    config = toml.load(config_path)
except Exception as e:
    st.error(f"Error loading config.toml: {e}")
    st.stop()

# Extract settings from config
GOOGLE_API_KEY = config['api'].get('google_api_key', None)
MODEL_NAME = config['settings'].get('model', 'text-bison-001')  # Default to text-bison-001

# Check if API key is found
if not GOOGLE_API_KEY:
    st.error("Google API key not found in the configuration file.")
    st.stop()

# Configure Streamlit page
st.set_page_config(page_title="Quantum Zeus 1.0", page_icon="⚡️", layout="centered")

# Configure Gemini API
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    # Directly initialize the selected model
    model = gen_ai.GenerativeModel(model_name=MODEL_NAME)
except Exception as e:
    st.error(f"Error initializing Gemini API: {e}")
    st.stop()

# Role mapping for display
def translate_role(role):
    return "assistant" if role == "model" else role

# Initialize session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Quantum NLP function using PennyLane
def run_quantum_nlp(user_prompt):
    try:
        # Set up the quantum device (PennyLane)
        dev = qml.device("default.qubit", wires=2)

        # Define a quantum circuit ansatz
        @qml.qnode(dev)
        def quantum_circuit():
            # Example quantum operations
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            return qml.state()

        # Execute the quantum circuit to simulate the quantum NLP process
        quantum_output = quantum_circuit()

        # Process the result
        return f"Quantum NLP processed the input and the result is: {quantum_output}"

    except Exception as e:
        return f"Error during Quantum NLP processing: {str(e)}"

# Title with "Powered by Gemini and Quantum NLP"
st.title("🤖 Quantum Zeus 1.0 (Powered by Google Gemini and Quantum NLP)")

# Chat history display
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)):
        st.markdown(message.parts[0].text if message.parts else "(empty)")

# Chat input
user_prompt = st.chat_input("Ask Zeus anything...")
if user_prompt:
    try:
        # Display user input
        st.chat_message("user").markdown(user_prompt)
        
        # Generate the response from Google Gemini API
        response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display the response from the assistant
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Trigger Quantum NLP if the user explicitly asks for it
        if "quantum nlp" in user_prompt.lower():
            quantum_nlp_result = run_quantum_nlp(user_prompt)
            st.write(f"Quantum NLP Result: {quantum_nlp_result}")
        else:
            st.write("No Quantum NLP triggered. Ask for it by saying 'quantum nlp'.")

    except Exception as e:
        st.error(f"Chat error: {e}")

