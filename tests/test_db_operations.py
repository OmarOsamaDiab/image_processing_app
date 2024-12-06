from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import init_db, SessionLocal
from app.models import ImageFrame
import pytest

DATABASE_URL = "mysql://root:password@localhost/image_db"

# Create a test session for database operations
engine = create_engine(DATABASE_URL)
SessionTest = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    init_db()
    db = SessionTest()
    yield db
    db.close()

def test_add_image_frame(setup_database):
    db = setup_database
    frame = ImageFrame(depth=50, image_data=b"testdata")
    db.add(frame)
    db.commit()
    assert frame.id is not None

def test_get_image_frames(setup_database):
    db = setup_database
    frames = db.query(ImageFrame).all()
    assert len(frames) > 0
    assert frames[0].depth == 50
