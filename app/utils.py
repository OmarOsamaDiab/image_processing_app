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
def apply_colormap(image_array):
    return cv2.applyColorMap(image_array, cv2.COLORMAP_JET)
