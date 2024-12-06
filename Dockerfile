FROM python:3.10

# Install system dependencies required for mysqlclient and OpenCV
RUN apt-get update && \
    apt-get install -y libmariadb-dev gcc \
    libgl1-mesa-glx libglib2.0-0

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
