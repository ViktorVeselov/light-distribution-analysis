# Light-Distribution-Analysis

## Overview

Light-Distribution-Analysis is a Python package designed for the analysis of light distribution in images. The package utilizes OpenCV, NumPy, and Matplotlib to enable in-depth yet simple analysis of the flux and power in images based on their wavelength and frequency representations.

## Features

- Convert RGB images to wavelength and frequency representations.
- Calculate the flux and power of images.
- Save processed images in various forms, including original, wavelength, frequency, and power images.
- Calculate similarity scores based on flux and power.
- Plot power images.
- Export flux and power data to a CSV file for further analysis (feature planned).

## Installation

To install Light-Distribution-Analysis, run the following command in your terminal:

```bash
pip install light-distribution-analysis
```

## Usage
Comparing Flux of Two Images
The package includes a function compare_flux that allows you to compare the flux of two images and obtain a similarity score.

Here's a simple example to demonstrate its usage:

## 1. Import the package:
```bash
import light_distribution_analysis as lda
```
## 2. Provide Paths to Images:

Provide the paths to the two images you want to compare.

```bash
image_path1 = "path/to/your/first/image.jpg"
image_path2 = "path/to/your/second/image.jpg"
```
## 3. Compare the Flux:

Use the compare_flux function to compare the flux of the two images.
```bash
similarity_score = lda.compare_flux(image_path1, image_path2)
```

## 4. Basic Image Processing
```bash
from light_distribution_analysis import process_single_image
process_single_image('path/to/image.jpg', 'output/directory/')
```
## 5. Flux Comparison
```bash
from light_distribution_analysis import compare_flux
similarity_score_flux = compare_flux('path/to/image1.jpg', 'path/to/image2.jpg')
print(f"Flux Similarity Score: {similarity_score_flux}")
```
## 6. Power Calculation and Comparison
```bash
from light_distribution_analysis import compare_power
similarity_score_power = compare_power('path/to/image1.jpg', 'path/to/image2.jpg')
print(f"Power Similarity Score: {similarity_score_power}")
```
Plotting Power Images
The power images will be saved in the specified directory when you run compare_power.

## Interpreting the Similarity Score:

A similarity score close to 1 indicates that the images are highly similar in terms of their flux, whereas a score close to 0 suggests they are dissimilar.