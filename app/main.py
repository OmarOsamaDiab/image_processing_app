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
    file_path = "data/image_data.csv"
    df = pd.read_csv(file_path)

    db = SessionLocal()
    try:
        with db.begin():  # Start a transaction
            for _, row in df.iterrows():
                depth = row["depth"]
                image_array = row.drop("depth").values.reshape(-1, 200)
                resized_image = resize_image(image_array, 150)
                colored_image = apply_colormap(resized_image)

                frame = ImageFrame(depth=depth, image_data=colored_image.tobytes())
                db.add(frame)
    except Exception as e:
        db.rollback()
        raise e
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
