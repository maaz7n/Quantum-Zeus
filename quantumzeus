import os
import streamlit as st
from dotenv import load_dotenv
import lambeq
import pennylane as qml
import numpy as np
from lambeq import BobcatParser, QuantumTrainer, SPSAOptimizer
from sklearn.preprocessing import LabelEncoder

# Load environment variables (optional)
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Quantum Zeus 1.0",
    page_icon="🧠",
    layout="centered",
)

# Initialize lambeq parser
try:
    parser = BobcatParser()
except Exception as e:
    st.error(f"Error initializing parser: {str(e)}")
    st.stop()

# Define quantum device (simulator)
n_qubits = 4  # Small for demo
dev = qml.device("default.qubit", wires=n_qubits)

# Quantum circuit for QNLP
@qml.qnode(dev)
def quantum_circuit(params, diagram):
    try:
        # Placeholder for diagram-to-circuit conversion (simplified)
        # In practice, use lambeq's PennylaneModel
        for i in range(n_qubits):
            qml.RX(params[i], wires=i)
            qml.RZ(params[i + n_qubits], wires=i)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[2, 3])
        return qml.expval(qml.PauliZ(0))  # Measure for classification
    except Exception as e:
        st.error(f"Quantum circuit error: {str(e)}")
        return 0.0

# Function to process text to quantum circuit
def text_to_circuit(text):
    try:
        diagram = parser.sentence2diagram(text, tokenised=False)
        return diagram
    except Exception as e:
        st.error(f"Error parsing text: {str(e)}")
        return None

# Training data
training_sentences = [
    ("I love it", "positive"),
    ("This is great", "positive"),
    ("I hate it", "negative"),
    ("This is bad", "negative"),
]
test_sentences = [("I like this", "positive"), ("It is awful", "negative")]

# Encode labels
label_encoder = LabelEncoder()
train_labels = label_encoder.fit_transform([label for _, label in training_sentences])
test_labels = label_encoder.transform([label for _, label in test_sentences])

# Convert sentences to diagrams
train_diagrams = [text_to_circuit(sentence) for sentence, _ in training_sentences]
test_diagrams = [text_to_circuit(sentence) for sentence, _ in test_sentences]
# Remove None values from failed parses
train_diagrams = [d for d in train_diagrams if d is not None]
train_labels = [train_labels[i] for i in range(len(training_sentences)) if train_diagrams[i] is not None]

# Initialize model parameters
params = np.random.randn(2 * n_qubits)

# Define loss function
def loss_fn(params, diagrams, labels):
    try:
        predictions = [quantum_circuit(params, d) for d in diagrams]
        return np.mean((np.array(predictions) - labels) ** 2)
    except Exception as e:
        st.error(f"Loss calculation error: {str(e)}")
        return float('inf')

# Train quantum model
try:
    opt = SPSAOptimizer(maxiter=100, a=0.2, c=0.3)  # Fixed parameter
    for i in range(100):
        params, loss = opt.step(lambda p: loss_fn(p, train_diagrams, train_labels), params)
        if i % 20 == 0:
            st.write(f"Step {i}, Loss: {loss:.4f}")
except Exception as e:
    st.error(f"Training error: {str(e)}")
    st.stop()

# Function to predict sentiment
def predict_sentiment(text, params):
    diagram = text_to_circuit(text)
    if diagram is None:
        return "unknown"
    try:
        pred = quantum_circuit(params, diagram)
        return "positive" if pred > 0 else "negative"
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return "unknown"

# Initialize chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chatbot title
st.title("🤖 Quantum Zeus 1.0 (POWERED BY QNLP)")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask Quantum Zeus 1.0...")
if user_prompt:
    try:
        # Display user message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Predict sentiment
        sentiment = predict_sentiment(user_prompt, params)
        response = f"Quantum Zeus thinks your input is {sentiment}!"

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Error processing input: {str(e)}")

# Display model performance
try:
    test_predictions = [predict_sentiment(sentence, params) for sentence, _ in test_sentences]
    test_accuracy = np.mean([pred == label for pred, (_, label) in zip(test_predictions, test_sentences) if pred != "unknown"])
    st.sidebar.write(f"Test Accuracy: {test_accuracy:.2%}")
except Exception as e:
    st.sidebar.write(f"Error calculating accuracy: {str(e)}")
