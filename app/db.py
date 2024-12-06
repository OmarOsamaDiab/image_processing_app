from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)  # Use the DATABASE_URL environment variable to connect to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize DB (create tables)
def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)
