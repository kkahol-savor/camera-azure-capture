from pypylon import pylon
import os
import cv2
import threading

class CameraConnector:
    def __init__(self, camera_index=0, width=1024, height=768):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.frame_number = 0
        self.output_dir = f"images_camera_{camera_index}"
        os.makedirs(self.output_dir, exist_ok=True)
        self._configure_camera()

    def _configure_camera(self):
        # Get the list of all attached devices
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        
        if len(devices) == 0:
            raise pylon.RuntimeException("No camera present.")
        
        # Create an instant camera object with the specific device
        self.camera = pylon.InstantCamera(tl_factory.CreateDevice(devices[self.camera_index]))
        
        self.camera.Open()
        self.camera.Width.SetValue(self.width)
        self.camera.Height.SetValue(self.height)
        self.camera.Close()

    def start_grabbing(self):
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_grabbing(self):
        self.camera.StopGrabbing()

    def get_frame(self):
        if self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                frame = image.GetArray()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                grabResult.Release()
                return frame
        return None

    def save_frame(self, frame):
        filename = os.path.join(self.output_dir, f"frame_{self.frame_number:04d}.png")
        cv2.imwrite(filename, frame)
        self.frame_number += 1

def show_combined_video(camera1, camera2):
    cv2.namedWindow('Combined Camera View', cv2.WINDOW_NORMAL)
    while camera1.camera.IsGrabbing() and camera2.camera.IsGrabbing():
        frame1 = camera1.get_frame()
        frame2 = camera2.get_frame()
        if frame1 is not None and frame2 is not None:
            camera1.save_frame(frame1)
            camera2.save_frame(frame2)
            combined_frame = cv2.hconcat([frame1, frame2])
            cv2.imshow('Combined Camera View', combined_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

def run_camera(camera_index, width, height):
    camera = CameraConnector(camera_index=camera_index, width=width, height=height)
    camera.start_grabbing()
    return camera

# Example usage
if __name__ == "__main__":
    # Initialize cameras
    camera1 = run_camera(0, 1024, 768)
    camera2 = run_camera(1, 1024, 768)

    # Create a thread to show combined video
    combined_video_thread = threading.Thread(target=show_combined_video, args=(camera1, camera2))

    # Start the thread
    combined_video_thread.start()

    # Wait for the thread to finish
    combined_video_thread.join()

    # Stop grabbing for both cameras
    camera1.stop_grabbing()
    camera2.stop_grabbing()