import streamlit as st
import google.generativeai as gen_ai
import os
from dotenv import load_dotenv
from quantum_nlp import run_quantum_nlp
from quantum_grover import run_quantum_grover
from quantum_database import query_quantum_database

# Load environment variables
load_dotenv('/Users/mohammedmazin/Downloads/quantum zeus/.env')


# Setup Google Gemini API Key
API_KEY = os.getenv('GOOGLE_API_KEY')
gen_ai.configure(api_key=API_KEY)

# Setup Streamlit page
st.set_page_config(page_title="Quantum Zeus", page_icon="⚡️", layout="centered")

# Initialize session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

# Role mapping for chat display
def translate_role(role):
    return "assistant" if role == "model" else role

# Process user query with Google Gemini and Quantum Systems (Quantum Processing on Every Prompt)
def process_user_query(user_prompt):
    # Trigger Quantum NLP for processing user query
    quantum_nlp_result = run_quantum_nlp(user_prompt)  # Run Quantum NLP

    # Perform Quantum Database Query to simulate quantum data processing
    quantum_db_result = query_quantum_database(['quantum_search'])  # Simulated quantum DB query using Qiskit

    # Run Grover's Algorithm if the input involves optimization or searching
    if "optimization" in user_prompt.lower() or "search" in user_prompt.lower():
        quantum_grover_result = run_quantum_grover('optimal solution')  # Run Grover's algorithm for optimization
    else:
        quantum_grover_result = "No optimization algorithm needed for this query."

    # Generate the final response by combining quantum results and NLP processing
    combined_result = (
        f"Quantum Processing Results:\n"
        f"- Quantum NLP Output: {quantum_nlp_result}\n"
        f"- Quantum Database Query Result: {quantum_db_result}\n"
        f"- Grover's Algorithm Optimization Result: {quantum_grover_result}"
    )

    # Send the result to Google Gemini for further human-like response generation
    gemini_response = gen_ai.generate_text(f"Interpret the following quantum result in human-friendly language: {combined_result}").text

    return gemini_response

# Title for the page
st.title("Quantum Zeus (Powered by Google Gemini and Quantum Computing)")

# Chat history display
for message in st.session_state.chat_session:
    with st.chat_message(translate_role(message['role'])):
        st.markdown(message['text'])

# User input
user_prompt = st.chat_input("Ask Quantum AI Assistant...")
if user_prompt:
    try:
        st.chat_message("user").markdown(user_prompt)

        # Process the user query with quantum system and Gemini
        response = process_user_query(user_prompt)

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add to chat session
        st.session_state.chat_session.append({"role": "user", "text": user_prompt})
        st.session_state.chat_session.append({"role": "assistant", "text": response})

    except Exception as e:
        st.error(f"Error: {e}")

