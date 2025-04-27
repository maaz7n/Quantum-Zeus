import pennylane as qml
import numpy as np
from lambeq import BobcatParser, IQPAnsatz, TketModel, remove_cups
from pytket.extensions.qiskit import AerBackend
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup lambeq parser
parser = BobcatParser()

# Define required parameters for IQPAnsatz
ob_map = {'N': 1, 'S': 1}  # Define atomic types for grammar
n_layers = 2               # Number of layers in the quantum circuit

# Initialize ansatz with object mapping and number of layers
ansatz = IQPAnsatz(ob_map=ob_map, n_layers=n_layers)

# Setup quantum backend and model
backend = AerBackend()
model = None

# Set up PennyLane device
dev = qml.device("default.qubit", wires=4)

# Define a quantum function to process lambeq quantum circuits with PennyLane
@qml.qnode(dev)
def execute_quantum_circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RX(params[2], wires=2)
    qml.CNOT(wires=[2, 3])
    qml.RY(params[3], wires=3)
    return qml.state()

def run_quantum_nlp(prompt):
    try:
        # Parse the sentence into a DisCoCat diagram
        diagrams = parser.sentence2diagram(prompt)
        if not diagrams:
            return "🚫 lambeq could not parse the sentence."

        # Simplify the diagram
        simplified = remove_cups(diagrams[0])

        # Apply ansatz to convert the diagram into a quantum circuit
        circuit = ansatz.normalise(simplified)

        # Initialize the model with the diagrams
        model = TketModel.from_diagrams([simplified], backend=backend, use_loss=False, normalize=True)

        # Assign dummy parameters for execution (real model would optimize/train)
        dummy_params = np.random.uniform(0, 2 * np.pi, size=4)

        # Execute the circuit on PennyLane simulator
        result = execute_quantum_circuit(dummy_params)

        # Also simulate with lambeq model (non-learning mode)
        model_output = model.evaluate(circuit)

        return (
            f"🔮 Quantum NLP executed full processing:\n"
            f"- 🧠 DisCoCat diagram: {simplified}\n"
            f"- 🧪 PennyLane state vector: {np.round(result, 3)}\n"
            f"- 🧪 lambeq model output: {model_output}"
        )

    except Exception as e:
        return f"❌ Full quantum NLP error: {str(e)}"

