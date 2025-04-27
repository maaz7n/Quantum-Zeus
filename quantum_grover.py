import numpy as np
import pennylane as qml

# Define the Grover's Algorithm for solving the problem
def grovers_algorithm(oracle, n_qubits):
    # Set up a PennyLane device
    dev = qml.device('default.qubit', wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        # Apply Hadamard gates to all qubits
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        
        # Apply the oracle
        oracle()

        # Apply Grover's Diffusion Operator
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
            qml.PauliX(wires=i)
        qml.MultiControlledX(wires=range(n_qubits), control_wires=[i for i in range(n_qubits - 1)])
        for i in range(n_qubits):
            qml.PauliX(wires=i)
            qml.Hadamard(wires=i)

        return qml.state()

    return circuit()

def run_quantum_grover(target_state):
    n_qubits = 4  # Number of qubits
    # Define a simple oracle that flips the target state
    def oracle():
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])

    result = grovers_algorithm(oracle, n_qubits)
    return f"Grover's Algorithm output (state vector): {np.round(result, 3)}"

