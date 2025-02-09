import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the connection string and container name from environment variables
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME')

class BlobHandler:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(CONTAINER_NAME)

    def upload_file(self, local_file_path, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Uploaded {local_file_path} to {blob_name}")

    def list_files(self):
        blob_list = self.container_client.list_blobs()
        for blob in blob_list:
            print(blob.name)

    def delete_file(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        print(f"Deleted {blob_name}")

    def delete_local_files(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted local file {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

# Example usage
if __name__ == "__main__":
    blob_handler = BlobHandler()
    # Upload a file
    blob_handler.upload_file("images_camera_0/frame_0001.png", "images_camera_0/frame_0001.png")
    # List files in the container
    blob_handler.list_files()
    # Delete a file from the container
    # blob_handler.delete_file("blob_name.png")
    # # Delete local files in a directory
    # blob_handler.delete_local_files("path/to/local/directory")