import sys
import os
import time
import threading
from yolo import YOLO

class FoodDetectionSystem:
    def __init__(self, user_settings, notification_system):
        self.user_settings = user_settings
        self.notification_system = notification_system
        self.yolo = None
        self.detection_thread = None

    def initialize_yolo(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), "detectionmodels", "yolo12l.pt")
            self.yolo = YOLO(
                camera_index=0,
                resolution=self.user_settings['camera_settings']['resolution'],
                frame_check_interval=self.user_settings['camera_settings']['frame_check_interval'],
                model_path=model_path,
                threshold=self.user_settings['threshold']
            )
            self.yolo.initialize_camera()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize YOLO: {str(e)}")

    def _detection_loop(self, running_flag):
        print("Detection started.")
        while running_flag['running']:
            frame = self.yolo.capture_image()
            if frame is not None:
                detected_objects = self.yolo.detect_objects(frame)
                for obj in detected_objects:
                    if obj in self.user_settings['objects_to_detect']:
                        self.notify_users(obj)
                if detected_objects:
                    print(f"Detected: {detected_objects}")
            time.sleep(self.user_settings['camera_settings']['frame_check_interval'])
        print("Detection stopped.")

    def start_detection(self, running_flag):
        if self.yolo is None:
            self.initialize_yolo()
        if self.detection_thread is None or not self.detection_thread.is_alive():
            running_flag['running'] = True
            self.detection_thread = threading.Thread(target=self._detection_loop, args=(running_flag,))
            self.detection_thread.start()
        else:
            print("Detection is already running in a separate thread.")

    def check_detections(self):
        if self.yolo is None:
            raise Exception("YOLO has not been initialized.")
        
        frame = self.yolo.capture_image()
        if frame is not None:
            detected_objects = self.yolo.detect_objects(frame)
            for obj in detected_objects:
                if obj in self.user_settings['objects_to_detect']:
                    self.notify_users(obj)
            return detected_objects
        return []

    def notify_users(self, detected_object):
        for user_id in self.user_settings['user_ids']:
            self.notification_system.notify(user_id, f"{detected_object} detected!")

    def release_camera(self):
        if self.yolo is not None:
            self.yolo.release_camera()