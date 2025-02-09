
# Camera Capture and Blob Storage System

## Overview

This project is designed to capture images from multiple cameras, display a combined video feed, and periodically upload the captured images to Azure Blob Storage. It also includes functionality to clear local image files after a specified interval.

## Features

- Capture images from multiple cameras (configurable resolution)
- Display combined camera feed
- Periodic upload of images to Azure Blob Storage
- Automated clearing of local image files

## Project Structure

- `blob_handler.py`: Handles uploading, listing, and deleting files from Azure Blob Storage.
- `camera_connector.py`: Manages camera configuration, image capture, and video display.
- `main_loop.py`: The main script that orchestrates camera operations, uploads, and file management.
- `requirements.txt`: Lists all Python dependencies.

## Prerequisites

- Python 3.x
- Cameras compatible with `pypylon`
- Azure Blob Storage account

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file with the following content:
   ```ini
   CONNECTION_STRING=your_azure_blob_connection_string
   CONTAINER_NAME=your_container_name
   CLEAR_INTERVAL_HOURS=12
   UPLOAD_INTERVAL_SECONDS=60
   SHOW_CAPTURE=True
   ```

## Usage

1. **Run the Main Script:**
   ```bash
   python main_loop.py
   ```

2. **Key Functionalities:**
   - Displays combined video feed from three cameras.
   - Captures and saves frames locally.
   - Periodically uploads images to Azure Blob Storage.
   - Clears local images based on the specified interval.

3. **Stopping the Program:**
   - Press `q` in the video window to stop the combined feed.
   - The program handles clean termination of all threads and camera resources.

## Configuration

- **Resolution:**
  - Default resolution is set to `2048x2048` in `main_loop.py`.
  - Can be modified by changing the `width` and `height` parameters in the `run_camera` function.

- **Intervals:**
  - Upload and clear intervals can be configured in the `.env` file.

## Troubleshooting

- **No Camera Detected:**
  - Ensure cameras are connected and drivers are properly installed.
  - Check permissions for accessing camera devices.

- **Azure Upload Issues:**
  - Verify the `CONNECTION_STRING` and `CONTAINER_NAME` in the `.env` file.
  - Ensure network connectivity to Azure services.

## Dependencies

- `pypylon`
- `opencv-python`
- `azure-storage-blob`
- `python-dotenv`
- See `requirements.txt` for the full list.

## License

This project is licensed under the MIT License.

## Author
Dr. Kanav Kahol