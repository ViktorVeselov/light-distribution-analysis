import logging
from qiskit.opflow import PauliSumOp


# Configure the logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s"
    )


# Validate that the input is a PauliSumOp
def validate_hamiltonian(hamiltonian):
    if not isinstance(hamiltonian, PauliSumOp):
        raise ValueError("Hamiltonian must be provided as a PauliSumOp instance.")
