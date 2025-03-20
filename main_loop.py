import threading
import time
import os
from datetime import datetime, timedelta
from camera_connector import run_camera, show_combined_video
from blob_handler import BlobHandler
from dotenv import load_dotenv
import cv2

# Load environment variables from .env file
load_dotenv()

# Retrieve the interval for clearing local files from environment variables
CLEAR_INTERVAL_HOURS = int(os.getenv('CLEAR_INTERVAL_HOURS', 12))
UPLOAD_INTERVAL_SECONDS = int(os.getenv('UPLOAD_INTERVAL_SECONDS', 60))
SHOW_CAPTURE = os.getenv('SHOW_CAPTURE', 'True').lower() == 'true'

def upload_images_periodically(blob_handler, directories, interval=UPLOAD_INTERVAL_SECONDS):
    last_upload_time = datetime.now() - timedelta(seconds=interval)
    
    while True:
        current_time = datetime.now()
        files_to_upload = []
        
        for directory in directories:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mod_time > last_upload_time:
                        files_to_upload.append((directory, filename, file_path))
        
        # Sort files by modification time
        files_to_upload.sort(key=lambda x: os.path.getmtime(x[2]))
        
        # Upload files alternatively from each directory
        for i in range(0, len(files_to_upload), len(directories)):
            for j in range(len(directories)):
                if i + j < len(files_to_upload):
                    directory, filename, file_path = files_to_upload[i + j]
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    blob_name = f"{directory}/{timestamp}_{filename}"
                    blob_handler.upload_file(file_path, blob_name)
                    print(f"Uploaded {file_path} to {blob_name}")
        
        last_upload_time = current_time
        time.sleep(interval)

def clear_local_images_periodically(directories, interval_hours):
    while True:
        time.sleep(interval_hours * 3600)
        for directory in directories:
            blob_handler.delete_local_files(directory)

def show_combined_video(camera1, camera2, camera3):
    c=1
    if SHOW_CAPTURE:
        cv2.namedWindow('Combined Camera View', cv2.WINDOW_NORMAL)
    while camera1.camera.IsGrabbing() and camera2.camera.IsGrabbing() and camera3.camera.IsGrabbing():
        frame1 = camera1.get_frame()
        frame2 = camera2.get_frame()
        frame3 = camera3.get_frame()
        if frame1 is not None and frame2 is not None and frame3 is not None:
            camera1.save_frame(frame1)
            camera2.save_frame(frame2)
            camera3.save_frame(frame3)
            if SHOW_CAPTURE:
                combined_frame = cv2.hconcat([frame1, frame2, frame3])
                cv2.imshow('Combined Camera View', combined_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print(f"Captured frames from all cameras iteration no: {c}")
                c=c+1
    if SHOW_CAPTURE:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Initialize cameras
    camera1 = run_camera(0, 2048, 2048)
    camera2 = run_camera(1, 2048, 2048)
    camera3 = run_camera(2, 2048, 2048)

    # Create a thread to show combined video
    combined_video_thread = threading.Thread(target=show_combined_video, args=(camera1, camera2, camera3))

    # Start the thread
    combined_video_thread.start()

    # Initialize BlobHandler
    blob_handler = BlobHandler()

    # Directories to monitor
    base_dir=os.getenv('OUTPUT_DIRECTORY')
    dir1=base_dir+'/images_camera_0'
    dir2=base_dir+'/images_camera_1'
    dir3=base_dir+'/images_camera_2'
    directories = [dir1, dir2, dir3]

    # Create a thread to upload images to Azure Blob Storage every minute
    upload_thread = threading.Thread(target=upload_images_periodically, args=(blob_handler, directories, UPLOAD_INTERVAL_SECONDS))

    # Create a thread to clear local images every CLEAR_INTERVAL_HOURS
    clear_thread = threading.Thread(target=clear_local_images_periodically, args=(directories, CLEAR_INTERVAL_HOURS))

    # Start the threads
    upload_thread.start()
    clear_thread.start()

    # Wait for the combined video thread to finish
    combined_video_thread.join()

    # Stop grabbing for all cameras
    camera1.stop_grabbing()
    camera2.stop_grabbing()
    camera3.stop_grabbing()

    # Wait for the upload and clear threads to finish
    upload_thread.join()
    clear_thread.join()