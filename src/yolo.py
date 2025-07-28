import cv2
import os
from ultralytics import YOLO as UltralyticsYOLO

class YOLO:
    def __init__(self, camera_index=0, resolution=(640, 480), frame_check_interval=1, model_path=None, threshold=0.5):
        self.camera_index = camera_index
        self.resolution = resolution
        self.frame_check_interval = frame_check_interval
        self.threshold = threshold
        self.camera = None
        self.fallback_frame = None
        self.model_path = model_path
        self.detected_objects = []
        try:
            self.model = UltralyticsYOLO(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load YOLO model: {str(e)}")

    def initialize_camera(self):
        self.camera = cv2.VideoCapture(self.camera_index)
        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            print("WARNING: Could not open webcam. Using fallback image.")
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            fallback_path = os.path.join(project_root, "data", "camera_replacement.jpg")
            if os.path.exists(fallback_path):
                self.fallback_frame = cv2.imread(fallback_path)
                if self.fallback_frame is None:
                    print("ERROR: Failed to load fallback image.")
            else:
                print(f"ERROR: Fallback image not found at {fallback_path}")
        else:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

    def capture_image(self):
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        elif self.fallback_frame is not None:
            return self.fallback_frame.copy()
        return None

    def detect_objects(self, frame):
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
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.fallback_frame = None

    def get_detected_objects(self):
        return self.detected_objects