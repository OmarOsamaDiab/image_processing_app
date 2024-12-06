import cv2
import numpy as np

# Resize the image to a new width while maintaining aspect ratio
def resize_image(image_array, new_width):
    aspect_ratio = image_array.shape[1] / image_array.shape[0]
    new_height = int(new_width / aspect_ratio)
    resized_image = cv2.resize(image_array, (new_width, new_height))
    return resized_image

# Apply a custom colormap to the image
def apply_colormap(image_array):
    return cv2.applyColorMap(image_array, cv2.COLORMAP_JET)
