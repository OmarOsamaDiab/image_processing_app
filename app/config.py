import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")  # Get the full database URL from the .env file
DB_USER = os.getenv("DB_USER")  # Get the database user
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Get the database password
DB_NAME = os.getenv("DB_NAME")  # Get the database name
