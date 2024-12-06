# Image Processing API

This is a FastAPI application that processes image data stored in a CSV file. The API provides endpoints to resize images and apply custom color maps. The processed images are stored in a MySQL database.

## Requirements
- Docker
- Docker Compose
- Python 3.10

## Setup and Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/image-processing-app.git
    cd image-processing-app
    ```

2. Build the Docker containers:

    ```bash
    docker-compose build
    ```

3. Start the containers:

    ```bash
    docker-compose up
    ```

4. Access the API at `http://localhost:8000`.

5. To run tests:

    ```bash
    docker-compose exec app pytest
    ```

## API Endpoints

- `GET /frames/`: Retrieve image frames by depth range.

    Query Parameters:
    - `depth_min`: Minimum depth.
    - `depth_max`: Maximum depth.
