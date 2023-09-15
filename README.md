# Light-Distribution-Analysis

[![CI](https://github.com/SweatyCrayfish/light-distribution-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/SweatyCrayfish/light-distribution-analysis/actions/workflows/ci.yml)

## Overview

Light-Distribution-Analysis is a Python package designed for the analysis of light distribution in images. The package utilizes OpenCV, NumPy, and Matplotlib to enable in-depth yet simple analysis of the flux and power in images based on their wavelength and frequency representations.

## Features

- Convert RGB images to wavelength and frequency representations
- Apply edge detection on images
- Calculate the flux and power of images
- Save processed images in various forms
- Calculate similarity scores based on flux and power
- Plot power images
- Export flux and power data to a CSV file (feature planned)

## Installation

To install Light-Distribution-Analysis, run the following command in your terminal:

```bash
python3 -m pip install light-distribution-analysis
```

## Functions

### Validate File Type

```bash
from light_distribution_analysis import validate_file_type
is_valid = validate_file_type('path/to/image.jpg')
```

Checks if the file type of an image is valid (JPG or PNG).

### Validate Image Dimensions

```bash
from light_distribution_analysis import validate_image_dimensions
is_valid = validate_image_dimensions(image_array)
```

Checks if an image has the correct dimensions (3-channel color image).

### Load Image

```bash
from light_distribution_analysis import load_image
image_array = load_image('path/to/image.jpg')
```

Loads an image from a given path into a NumPy array.

### Convert to RGB

```bash
from light_distribution_analysis import convert_to_rgb
image_rgb = convert_to_rgb(image_array)
```

Converts a given image to its RGB representation.

### Save Image

```bash
from light_distribution_analysis import save_image
save_image(image_array, 'path/to/save/image.jpg')
```

Saves an image to the specified path.

### Apply Edge Detection

```bash
from light_distribution_analysis import apply_edge_detection
edge_image = apply_edge_detection(image_array, method='Canny')
```

Applies edge detection to an image using either the 'Canny' or 'Sobel' method.

### Calculate Flux

```bash
from light_distribution_analysis import calculate_flux
flux_value = calculate_flux(intensity_image, quantity_image)
```

Calculates the flux of an image given its intensity and quantity representations.

### Calculate Power

```bash
from light_distribution_analysis import calculate_power
power_value = calculate_power(intensity_image)
```

Calculates the power of an image based on its intensity representation.

### Plot Power Image

```bash
from light_distribution_analysis import plot_power_image
plot_power_image(intensity_image, 'path/to/save/power_image.jpg')
```

Generates and saves a power image based on the intensity of the original image.

## Examples

### Basic Image Processing

```bash
from light_distribution_analysis import process_single_image
process_single_image('path/to/image.jpg', 'output/directory/')
```

### Flux Comparison

```bash
from light_distribution_analysis import compare_flux
similarity_score_flux = compare_flux('path/to/image1.jpg', 'path/to/image2.jpg')
print(f"Flux Similarity Score: {similarity_score_flux}")
```

### Power Calculation and Comparison

```bash
from light_distribution_analysis import compare_power
similarity_score_power = compare_power('path/to/image1.jpg', 'path/to/image2.jpg')
print(f"Power Similarity Score: {similarity_score_power}")
```

## Interpreting the Similarity Score

A similarity score close to 1 indicates that the images are highly similar in terms of their flux, whereas a score close to 0 suggests they are dissimilar.
