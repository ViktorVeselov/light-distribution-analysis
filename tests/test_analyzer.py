import unittest
import numpy as np
from light_distribution_analysis import analyzer


class TestAnalyzer(unittest.TestCase):
    def test_calculate_flux(self):
        intensity = np.array([1, 2, 3])
        quantity = np.array([1, 2, 3])
        expected_flux = 14  # 1*1 + 2*2 + 3*3 = 1 + 4 + 9 = 14

        result = analyzer.calculate_flux(intensity, quantity)
        self.assertEqual(result, expected_flux)


if __name__ == "__main__":
    unittest.main()
