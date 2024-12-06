import cv2
import numpy as np
from skimage.transform import resize

# Resize the image to a new width while maintaining aspect ratio
def resize_image(image_array: np.ndarray, target_height: int, target_width: int) -> np.ndarray:
    """
    Resize an image represented as a numpy array to the target height and width.
    """
    resized_image = resize(image_array, (target_height, target_width), mode='reflect', anti_aliasing=True)
    return resized_image
# Apply a custom colormap to the image
def apply_colormap(image):
    # Ensure the image is in uint8 format and scaled between 0-255
    image = np.array(image, dtype=np.uint8)

    # If it's a single-channel (grayscale) image, ensure it's 2D
    if len(image.shape) == 2:
        return cv2.applyColorMap(image, cv2.COLORMAP_JET)
    
    # If it's a 3-channel image (color), apply the colormap to each channel
    elif len(image.shape) == 3 and image.shape[2] == 3:
        return cv2.applyColorMap(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_JET)
    
    # If the image has unexpected shape, raise an error
    else:
        raise ValueError("Image must be either 2D (grayscale) or 3D (color)")
