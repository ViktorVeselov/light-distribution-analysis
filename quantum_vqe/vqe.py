from qiskit import Aer, execute
from qiskit.opflow import StateFn, PauliExpectation, CircuitSampler, PauliSumOp
from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.utils import QuantumInstance
from scipy.optimize import minimize
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s"
)  # Set up configuration for logging


def expectation_value(circuit, parameters, hamiltonian, backend):
    try:
        if not isinstance(hamiltonian, PauliSumOp):
            raise ValueError("Hamiltonian must be provided as a PauliSumOp instance.")
        quantum_instance = QuantumInstance(backend)
        param_dict = dict(
            zip(circuit.parameters, parameters)
        )  # Construct the circuit with the given parameters
        bound_circuit = circuit.bind_parameters(param_dict)
        expectation = StateFn(hamiltonian, is_measurement=True).compose(
            StateFn(bound_circuit)
        )  # Set up the expectation value calculation using PauliExpectation
        pauli_expectation = AerPauliExpectation().convert(expectation)
        sampler = CircuitSampler(quantum_instance).convert(pauli_expectation)
        # Evaluate the expectation value
        return np.real(sampler.eval())
    except Exception as e:
        logging.error("Failed to compute expectation value: %s", e)
        raise


def create_vqe_ansatz(num_qubits):
    parameters = [Parameter(f'θ{i}') for i in range(num_qubits)]
    circuit = QuantumCircuit(num_qubits) # Create a quantum circuit with the given number of qubits
    for qubit in range(num_qubits): # Add a Hadamard gate to each qubit to create a superposition
        circuit.h(qubit)
    for i, parameter in enumerate(parameters): # Add parameterized rotation around the Y axis for each qubit
        circuit.ry(parameter, i)
    for i in range(num_qubits - 1): # Entangle the qubits with a linear chain of CNOT gates
        circuit.cx(i, i + 1)
    return circuit, parameters




def optimize_vqe(circuit, hamiltonian, backend, optimizer="COBYLA"):
    try:
        if not isinstance(hamiltonian, PauliSumOp):  # Validate the Hamiltonian
            raise ValueError("Hamiltonian must be provided as a PauliSumOp instance.")

        def objective_function(params):
            try:
                return expectation_value(circuit, params, hamiltonian, backend)
            except Exception as e:
                logging.error("Objective function failed: %s", e)
                raise

        initial_params = np.random.rand(len(circuit.parameters))
        result = minimize(objective_function, initial_params, method=optimizer)
        return result
    except ValueError as e:
        logging.error("Input validation failed: %s", e)
        raise
    except Exception as e:
        logging.error("Optimization failed: %s", e)
        raise
