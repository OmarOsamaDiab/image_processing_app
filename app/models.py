from sqlalchemy import Column, Integer, LargeBinary
from app.db import Base

class ImageFrame(Base):
    __tablename__ = 'image_frames'

    id = Column(Integer, primary_key=True, index=True)
    depth = Column(Integer, index=True)
    image_data = Column(LargeBinary)
