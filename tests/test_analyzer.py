import unittest
from light_distribution_analysis import analyzer  # Replace with your actual import

class TestAnalyzer(unittest.TestCase):

    def test_calculate_flux(self):
        intensity = [1, 2, 3]
        quantity = [1, 2, 3]
        expected_flux = 14  # 1*1 + 2*2 + 3*3 = 1 + 4 + 9 = 14

        result = analyzer.calculate_flux(intensity, quantity)  # Replace with your actual function
        self.assertEqual(result, expected_flux)

if __name__ == '__main__':
    unittest.main()
