import unittest
import numpy as np
import os
import cv2
from light_distribution_analysis import validate_image_dimensions, validate_file_type, load_image


class TestImageProcessingFunctions(unittest.TestCase):
    def test_validate_image_dimensions(self):
        # Test for 3 channel image
        image = np.zeros((5, 5, 3), dtype=np.uint8)
        self.assertTrue(validate_image_dimensions(image))

        # Test for non 3 channel image
        image = np.zeros((5, 5), dtype=np.uint8)
        self.assertFalse(validate_image_dimensions(image))

    def test_validate_file_type(self):
        self.assertTrue(validate_file_type("test.jpg"))
        self.assertTrue(validate_file_type("test.jpeg"))
        self.assertTrue(validate_file_type("test.png"))
        self.assertFalse(validate_file_type("test.txt"))

    def test_load_image(self):
        # Create a test image
        test_image_path = "test_image.jpg"
        cv2.imwrite(test_image_path, np.zeros((5, 5, 3), dtype=np.uint8))

        self.assertIsNotNone(load_image(test_image_path))

        # Clean up
        os.remove(test_image_path)


if __name__ == "__main__":
    unittest.main()
