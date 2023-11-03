import unittest
from qiskit.opflow import PauliSumOp, X, Z, I
from qiskit import Aer
from vqe import create_vqe_ansatz, optimize_vqe

class TestVQE(unittest.TestCase):
    def test_create_vqe_ansatz(self):
        """Test if the VQE ansatz is created correctly."""
        num_qubits = 2
        circuit, parameters = create_vqe_ansatz(num_qubits)
        self.assertEqual(len(parameters), num_qubits)
        self.assertEqual(circuit.num_qubits, num_qubits)

    def test_optimize_vqe(self):
        """Test if the VQE optimization returns a result."""
        hamiltonian = (X ^ X) + (Z ^ I)
        backend = Aer.get_backend('statevector_simulator')
        circuit, parameters = create_vqe_ansatz(2)
        
        result = optimize_vqe(circuit, hamiltonian, backend)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()

