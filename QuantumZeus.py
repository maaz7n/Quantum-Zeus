import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import pennylane as qml
import numpy as np
from lambeq import BobcatParser
from sklearn.preprocessing import LabelEncoder

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

# Initialize Quantum NLP Parser (Lambeq)
parser = BobcatParser()

# Define quantum device (simulator)
n_qubits = 4  # Small for demo
dev = qml.device("default.qubit", wires=n_qubits)

# Quantum circuit for QNLP
@qml.qnode(dev)
def quantum_circuit(params):
    for i in range(n_qubits):
        qml.RX(params[i], wires=i)
        qml.RZ(params[i + n_qubits], wires=i)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[2, 3])
    return qml.expval(qml.PauliZ(0))  # Measure for classification

# Convert text to quantum circuit (using Lambeq)
def text_to_circuit(text):
    try:
        diagram = parser.sentence2diagram(text, tokenised=False)
        return diagram
    except Exception as e:
        st.error(f"Error parsing text: {str(e)}")
        return None

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("🤖 Quantum Zeus 1.0 (Powered by Google Gemini & Quantum NLP)")

# Chat history display
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text if message.parts else "(empty)")

# Chat input
user_prompt = st.chat_input("Ask Zeus anything...")
if user_prompt:
    try:
        st.chat_message("user").markdown(user_prompt)
        # Apply Quantum NLP processing (dummy quantum circuit optimization)
        diagram = text_to_circuit(user_prompt)
        if diagram:
            # Simplified: generate quantum-based prediction based on the input
            params = np.random.randn(2 * n_qubits)
            response = quantum_circuit(params)
            st.chat_message("assistant").markdown(f"Quantum Zeus processed your input. Result: {response:.4f}")
        else:
            # Fallback to standard Gemini response
            response = st.session_state.chat_session.send_message(user_prompt)
            st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Chat error: {e}")
