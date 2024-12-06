import numpy as np
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from app.models import ImageFrame
from app.utils import resize_image, apply_colormap
import pandas as pd

app = FastAPI(
    title="Image Processing API",
    description="This API processes image data stored in CSV format. It supports image resizing and applying a custom color map. The processed images are stored in a MySQL database.",
    version="1.0.0",
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def process_csv():
    """
    On startup, the application processes the image data CSV file, resizes and applies a color map to each frame,
    and stores the processed image data in the database.
    """
    init_db()
    file_path = "data/image_data.csv"  # Adjust the file path if needed

    # Load the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {str(e)}")

    # Start a database session
    db = SessionLocal()
    try:
        with db.begin():
            for _, row in df.iterrows():
                depth = row['depth']  # Get the depth value
                pixel_values = row[1:].values  # Extract pixel values (columns 1 to 200)
                
                # If depth is NaN, replace with default value (e.g., 0)
                if np.isnan(depth):
                    print(f"Warning: Found NaN for depth {depth}. Replacing with default value 0.")
                    depth = 0  # You can replace this with any other value you prefer

                # Ensure the pixel values are of correct length (200 in this case)
                if len(pixel_values) != 200:
                    print(f"Skipping row due to incorrect number of pixel values (expected 200, got {len(pixel_values)})")
                    continue  # Skip this row if the number of pixel values is incorrect

                # Debug: check the first few pixel values
                print(f"Processing depth {depth} with pixel values:", pixel_values[:10])  # Just print the first 10 pixel values

                # Reshape the pixel values into a 2D array (10x20 image)
                try:
                    image_array = pixel_values.reshape((10, 20))  # Or (20, 10) depending on actual data
                except ValueError as e:
                    print(f"Skipping row with depth {depth} due to reshaping error: {e}")
                    continue  # Skip if reshaping fails

                # Check if there are any NaN or infinite values in the image
                if np.any(np.isnan(image_array)) or np.any(np.isinf(image_array)):
                    print(f"Warning: NaN or infinite values found in image for depth {depth}. Replacing with default values.")
                    image_array = np.nan_to_num(image_array, nan=0, posinf=255, neginf=0)  # Replace invalid values

                # Resize image to width 150 and adjust height to maintain aspect ratio
                resized_image = resize(image_array, (10, 15), mode='reflect')  # Resize width to 150 pixels

                # Apply custom colormap
                colored_image = apply_colormap(resized_image)

                # Convert image to bytes (PNG format)
                pil_image = Image.fromarray((colored_image * 255).astype(np.uint8))  # Convert to PIL image
                with BytesIO() as byte_io:
                    pil_image.save(byte_io, format="PNG")
                    byte_data = byte_io.getvalue()

                # Store image data into the database
                frame = ImageFrame(depth=depth, image_data=byte_data)
                db.add(frame)

                # Debug: Print out the stored image depth and check if it's added
                print(f"Stored frame for depth {depth}.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing CSV data: {str(e)}")
    finally:
        db.close()

@app.get("/frames/", response_model=list, summary="Get Image Frames", description="Retrieve image frames in a specified depth range.")
def get_frames(depth_min: int, depth_max: int, db: Session = Depends(get_db)):
    """
    Get image frames based on a minimum and maximum depth range.
    """
    frames = db.query(ImageFrame).filter(ImageFrame.depth.between(depth_min, depth_max)).all()
    if not frames:
        raise HTTPException(status_code=404, detail="No frames found in the specified range.")
    
    return [{"depth": frame.depth, "image_data": frame.image_data} for frame in frames]
