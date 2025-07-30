"""
YOLO object detection wrapper module.

This module provides a wrapper around the Ultralytics YOLO model for real-time
object detection using camera input.
"""

import cv2
from ultralytics import YOLO as UltralyticsYOLO

class YOLO:
    """
    A wrapper class for YOLO object detection with camera integration.
    
    This class handles camera initialization, frame capture, and object detection
    using the Ultralytics YOLO model. It provides methods to configure detection
    parameters and retrieve detected objects.
    
    Attributes:
        camera_index (int): Index of the camera device to use.
        resolution (tuple): Camera resolution as (width, height).
        frame_check_interval (int): Interval between frame checks in seconds.
        threshold (float): Confidence threshold for object detection.
        camera (cv2.VideoCapture): OpenCV camera object.
        model_path (str): Path to the YOLO model file.
        detected_objects (list): List of recently detected objects.
        model (UltralyticsYOLO): Loaded YOLO model instance.
    """
    def __init__(self, camera_index=0, resolution=(640, 480), frame_check_interval=1, model_path=None, threshold=0.5):
        """
        Initialize the YOLO detection system.
        
        Args:
            camera_index (int, optional): Camera device index. Defaults to 0.
            resolution (tuple, optional): Camera resolution (width, height). Defaults to (640, 480).
            frame_check_interval (int, optional): Seconds between frame checks. Defaults to 1.
            model_path (str, optional): Path to YOLO model file. Defaults to None.
            threshold (float, optional): Detection confidence threshold. Defaults to 0.5.
            
        Raises:
            RuntimeError: If the YOLO model fails to load.
        """
        self.camera_index = camera_index
        self.resolution = resolution
        self.frame_check_interval = frame_check_interval
        self.threshold = threshold
        self.camera = None
        self.model_path = model_path
        self.detected_objects = []
        try:
            self.model = UltralyticsYOLO(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLO model: {str(e)}")

    def initialize_camera(self):
        """
        Initialize and configure the camera for video capture.
        
        Sets up the camera with the specified resolution and checks if it's
        accessible. Must be called before capturing frames.
        
        Raises:
            RuntimeError: If the camera cannot be opened or accessed.
        """
        self.camera = cv2.VideoCapture(self.camera_index)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        if not self.camera.isOpened():
            raise RuntimeError("Error: Could not open webcam.")

    def capture_image(self):
        """
        Capture a single frame from the camera.
        
        Returns:
            numpy.ndarray or None: The captured frame as a numpy array, or None if
                capture fails or camera is not initialized.
        """
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def detect_objects(self, frame):
        """
        Perform object detection on a given frame.
        
        Runs the YOLO model on the input frame and returns a list of detected
        objects that meet the confidence threshold.
        
        Args:
            frame (numpy.ndarray): Input image frame for object detection.
            
        Returns:
            list: List of detected object names (strings) that meet the threshold.
                Returns empty list if detection fails or no objects found.
        """
        try:
            results = self.model(frame)
            detected = set()
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0]) # 0 means the most propable object detected in box
                    label = self.model.names[cls_id]
                    if box.conf[0] >= self.threshold:  
                        detected.add(label)
            self.detected_objects = list(detected)
            return self.detected_objects
        except Exception as e:
            print(f"Error in object detection: {str(e)}")
            return []

    def release_camera(self):
        """
        Release the camera resource.
        
        Properly closes the camera connection to free up the resource for other
        applications. Should be called when done with detection.
        """
        if self.camera is not None:
            self.camera.release()
            self.camera = None # super

    def get_detected_objects(self):
        """
        Get the list of objects detected in the most recent detection.
        
        Returns:
            list: List of detected object names from the last detection operation.
        """
        return self.detected_objects