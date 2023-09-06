import logging
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)

# Function to validate the dimensions of an image
def validate_image_dimensions(image):
    """Check if an image has the correct dimensions (3-channel color image).

    Parameters:
        image (np.array): The image array.

    Returns:
        bool: True if image is valid, False otherwise.
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        logging.error("Invalid image dimensions. Expecting a 3-channel color image.")
        return False
    return True

def validate_file_type(file_path):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not any(file_path.endswith(ext) for ext in valid_extensions):
        logging.error(f"Invalid file type. Supported file types are {', '.join(valid_extensions)}")
        return False
    return True


# Function to load an image from a file path
def load_image(image_path):
    """Load an image from a given path using OpenCV.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        np.array: Loaded image array or None if loading fails.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            logging.error(f"Image at {image_path} could not be loaded.")
            return None
        logging.info(f"Successfully loaded the image from {image_path}.")
        return image
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to convert image to RGB
def convert_to_rgb(image):
    """Convert a BGR image to RGB.

    Parameters:
        image (np.array): The BGR image array.

    Returns:
        np.array: RGB image array or None if conversion fails.
    """
    try:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        logging.info("Successfully converted the image to RGB.")
        return rgb_image
    except Exception as e:
        logging.error(f"Failed to convert image to RGB: {e}")

def rgb_to_wavelength(r, g, b):
        """Convert RGB values to a wavelength in the visible spectrum.

    Parameters:
        r (int): Red channel value (0-255).
        g (int): Green channel value (0-255).
        b (int): Blue channel value (0-255).

    Returns:
        float: Wavelength in nanometers.
    """
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    hue = 0

    if max_val == min_val:
        hue = 0
    elif max_val == r:
        hue = (60 * ((g - b) / (max_val - min_val)) + 360) % 360
    elif max_val == g:
        hue = (60 * ((b - r) / (max_val - min_val)) + 120) % 360
    elif max_val == b:
        hue = (60 * ((r - g) / (max_val - min_val)) + 240) % 360

    if 0 <= hue < 60:
        return 620 + (hue / 60) * (740 - 620)
    elif 60 <= hue < 180:
        return 495 + ((hue - 60) / 120) * (570 - 495)
    elif 180 <= hue < 300:
        return 450 + ((hue - 180) / 120) * (495 - 450)
    else:
        return 620 + ((hue - 300) / 60) * (740 - 620)

def wavelength_to_frequency(wavelength):
        """Convert wavelength to frequency.

    Parameters:
        wavelength (float): Wavelength in meters.

    Returns:
        float: Frequency in Hz.
    """
    c = 299792458 
    return c / wavelength

def save_image(image, path, cmap=None):
        """Save an image to a specified file path.

    Parameters:
        image (np.array): Image data array.
        path (str): Destination file path.
        cmap (str, optional): Colormap to apply.

    Exceptions:
        Logs an error message if image saving fails.
    """
    try:
        plt.imshow(image, cmap=cmap)
        plt.axis('off')
        plt.savefig(path, bbox_inches='tight', pad_inches=0)
        plt.close()
    except Exception as e:
        logging.error(f"Failed to save image: {e}")

def apply_edge_detection(image, method='Canny'):
     """Apply edge detection to an image using either the Canny or Sobel algorithm.

    Parameters:
        image (np.array): Input image array.
        method (str): The method of edge detection ('Canny' or 'Sobel').

    Returns:
        np.array: Edge-detected image.

    Exceptions:
        Raises ValueError for an unknown method.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if method == 'Canny':
        return cv2.Canny(gray_image, 100, 200)
    elif method == 'Sobel':
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
        return np.sqrt(sobelx**2 + sobely**2)
    else:
        raise ValueError(f"Unknown method: {method}")


def save_transformed_image(image, transformation_type, final_dir, image_path):
    """Save a transformed image.

    Parameters:
        image (np.array): Transformed image array.
        transformation_type (str): The type of image transformation applied.
        final_dir (str): Directory to save the transformed image.
        image_path (str): Original image path.

    """
    save_image(image, f'{final_dir}/{transformation_type}_{os.path.basename(image_path)}')

def process_image_to_rgb(image_path, final_dir):
    """Process and save an image in RGB, wavelength, and frequency formats.

    Parameters:
        image_path (str): Path to the original image.
        final_dir (str): Directory to save the processed images.

    Exceptions:
        Logs an error message for invalid file type or image dimensions.
    """
    if not validate_file_type(image_path):
        return

    image = load_image(image_path)
    if image is None or not validate_image_dimensions(image):
        return

    image_rgb = convert_to_rgb(image)
    if image_rgb is None:
        return

    save_transformed_image(image_rgb, 'rgb', final_dir, image_path)
    logging.info(f"Processed and saved RGB image to {final_dir}.")
    wavelength_image = np.apply_along_axis(lambda x: rgb_to_wavelength(x[0], x[1], x[2]), axis=2, arr=image_rgb) * 1e-9
    frequency_image = wavelength_to_frequency(wavelength_image)
    save_image(wavelength_image * 1e9, f'{final_dir}/wavelength_{os.path.basename(image_path)}', cmap='nipy_spectral')
    save_image(frequency_image / 1e12, f'{final_dir}/frequency_{os.path.basename(image_path)}', cmap='jet')

def ltd(path_to_image_1, path_to_image_2, final_dir='final_dir'):
    """High-level function to process two images.

    Parameters:
        path_to_image_1 (str): Path to the first image.
        path_to_image_2 (str): Path to the second image.
        final_dir (str, optional): Directory to save the processed images.
    """
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    process_single_image(path_to_image_1, final_dir)
    process_single_image(path_to_image_2, final_dir)

def process_single_image(image_path, final_dir):
     """Process and save a single image in RGB, wavelength, and frequency formats.

    Parameters:
        image_path (str): Path to the original image.
        final_dir (str): Directory to save the processed images.

    Exceptions:
        Logs an error message for invalid file type or image dimensions.
    """
    if not validate_file_type(image_path):
        return
    image = load_image(image_path)
    if image is None or not validate_image_dimensions(image):
        return
    image_rgb = convert_to_rgb(image)
    if image_rgb is None:
        return
    save_image(image_rgb, f'{final_dir}/rgb_{os.path.basename(image_path)}')
    wavelength_image = np.apply_along_axis(lambda x: rgb_to_wavelength(x[0], x[1], x[2]), axis=2, arr=image_rgb) * 1e-9
    wavelength_image = np.array([wavelength for wavelength in tqdm(wavelength_image.flatten(), desc="Calculating Wavelengths", unit="pixel")]).reshape(wavelength_image.shape)
    frequency_image = wavelength_to_frequency(wavelength_image)
    save_image(wavelength_image * 1e9, f'{final_dir}/wavelength_{os.path.basename(image_path)}', cmap='nipy_spectral')
    save_image(frequency_image / 1e12, f'{final_dir}/frequency_{os.path.basename(image_path)}', cmap='jet')

def calculate_flux(intensity_image, quantity_image):
    """Calculate the flux of an image.

    Parameters:
        intensity_image (np.array): Intensity image array.
        quantity_image (np.array): Quantity image array (usually same as intensity).

    Returns:
        float: Total flux.
    """
    flux_image = intensity_image * quantity_image
    return np.sum(flux_image)

def calculate_power(intensity_image):
     """Calculate the power of an image.

    Parameters:
        intensity_image (np.array): Intensity image array.

    Returns:
        float: Total power.
    """
    power_image = intensity_image ** 2
    return np.sum(power_image)

def plot_power_image(intensity_image, save_path):
    """Plot and save the power image.

    Parameters:
        intensity_image (np.array): Intensity image array.
        save_path (str): Path to save the power image.

    """
    power_image = intensity_image ** 2
    plt.imshow(power_image, cmap='hot')
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def compare_flux(image_path1, image_path2, final_dir='comparison_results'):
    """Compare the flux of two images.

    Parameters:
        image_path1 (str): Path to the first image.
        image_path2 (str): Path to the second image.
        final_dir (str, optional): Directory to save comparison results.

    Returns:
        float: Flux similarity score.
    """
    process_single_image(image_path1, final_dir)
    process_single_image(image_path2, final_dir)
    intensity_image1 = cv2.imread(f"{final_dir}/frequency_{os.path.basename(image_path1)}.png", cv2.IMREAD_GRAYSCALE)
    intensity_image2 = cv2.imread(f"{final_dir}/frequency_{os.path.basename(image_path2)}.png", cv2.IMREAD_GRAYSCALE)
    flux1 = calculate_flux(intensity_image1, intensity_image1)
    flux2 = calculate_flux(intensity_image2, intensity_image2) 
    similarity_score_flux = 1 - abs(flux1 - flux2) / max(flux1, flux2)
    return similarity_score_flux

def compare_power(image_path1, image_path2, final_dir='comparison_results'):
    """Compare the power of two images.

    Parameters:
        image_path1 (str): Path to the first image.
        image_path2 (str): Path to the second image.
        final_dir (str, optional): Directory to save comparison results.

    Returns:
        float: Power similarity score.
    """
    process_single_image(image_path1, final_dir)
    process_single_image(image_path2, final_dir)
    intensity_image1 = cv2.imread(f"{final_dir}/frequency_{os.path.basename(image_path1)}.png", cv2.IMREAD_GRAYSCALE)
    intensity_image2 = cv2.imread(f"{final_dir}/frequency_{os.path.basename(image_path2)}.png", cv2.IMREAD_GRAYSCALE) 
    power1 = calculate_power(intensity_image1)
    power2 = calculate_power(intensity_image2)
    plot_power_image(intensity_image1, f"{final_dir}/power_{os.path.basename(image_path1)}.png")
    plot_power_image(intensity_image2, f"{final_dir}/power_{os.path.basename(image_path2)}.png")
    similarity_score_power = 1 - abs(power1 - power2) / max(power1, power2)
    return similarity_score_power



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Processing Utility")
    
    parser.add_argument("--image1", help="Path to the first image")
    parser.add_argument("--image2", help="Path to the second image")
    parser.add_argument("--outdir", default="final_dir", help="Output directory for processed images")
    parser.add_argument("--imagedir", help="Directory containing multiple images to process")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    if args.imagedir:
        image_files = [f for f in os.listdir(args.imagedir) if f.endswith(('jpg', 'png'))]
        for image_file in image_files:
            process_single_image(os.path.join(args.imagedir, image_file), args.outdir)
    elif args.image1 and args.image2:
        similarity_flux = compare_flux(args.image1, args.image2, args.outdir)
        similarity_power = compare_power(args.image1, args.image2, args.outdir)
        print(f"Flux Similarity Score: {similarity_flux}")
        print(f"Power Similarity Score: {similarity_power}")
    else:
        print("Either --imagedir or both --image1 and --image2 must be specified.")




