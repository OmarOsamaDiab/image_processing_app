import numpy as np
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
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
        with db.begin():  # Start a transaction for processing and storing images
            for _, row in df.iterrows():
                # Extract depth
                depth = row["depth"]

                # Extract image data by dropping the 'depth' column and converting the remaining values into a numpy array
                image_array = row.drop("depth").values
                num_pixels = image_array.shape[0]

                # Resize to the desired fixed dimensions (e.g., 150x150)
                try:
                    # Resize the image directly to 150x150 using the resize_image function
                    resized_image = resize_image(image_array, target_height=150, target_width=150)

                    # Apply the color map
                    colored_image = apply_colormap(resized_image)

                    # Create an ImageFrame object and store in the database
                    frame = ImageFrame(depth=depth, image_data=colored_image.tobytes())
                    db.add(frame)
                except Exception as e:
                    # Handle image resize or colormap errors without skipping the entire row
                    print(f"Error processing depth {depth}: {str(e)}")
                    continue  # Continue processing next frame even if there is an error with this one

    except Exception as e:
        db.rollback()  # Rollback if any error occurs during the transaction
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
