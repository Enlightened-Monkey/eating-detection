"""
Food detection system module.

This module provides the main food detection system that coordinates between
the YOLO model, camera input, and notification system for real-time object
detection and alert generation.
"""

import sys
import os
import time
import threading
from yolo import YOLO

class FoodDetectionSystem:
    """
    Main food detection system coordinator.
    
    This class manages the detection process by coordinating between the YOLO
    model, camera input, and notification system. It runs detection in a separate
    thread and sends notifications when target objects are detected.
    
    Attributes:
        user_settings (dict): Configuration settings for detection.
        notification_system (NotificationSystem): System for sending notifications.
        yolo (YOLO): YOLO detection model instance.
        detection_thread (Thread): Thread running the detection loop.
    """
    def __init__(self, user_settings, notification_system):
        """
        Initialize the food detection system.
        
        Args:
            user_settings (dict): Configuration settings including detection targets,
                thresholds, and camera settings.
            notification_system (NotificationSystem): System for sending notifications
                when objects are detected.
        """
        self.user_settings = user_settings
        self.notification_system = notification_system
        self.yolo = None
        self.detection_thread = None

    def initialize_yolo(self):
        """
        Initialize the YOLO detection model with current settings.
        
        Creates and configures a YOLO instance with the camera settings and
        detection parameters from user_settings. Downloads the model if needed.
        
        Raises:
            RuntimeError: If YOLO initialization fails due to model loading
                or camera initialization errors.
        """
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
        """
        Main detection loop that runs in a separate thread.
        
        Continuously captures frames from the camera, performs object detection,
        and sends notifications when target objects are found. Runs until the
        running_flag is set to False.
        
        Args:
            running_flag (dict): Dictionary with 'running' key to control loop execution.
        """
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
        """
        Start the object detection process in a separate thread.
        
        Initializes YOLO if needed and starts the detection loop in a background
        thread. If detection is already running, prints a message instead.
        
        Args:
            running_flag (dict): Dictionary with 'running' key to control detection loop.
        """
        if self.yolo is None:
            self.initialize_yolo()
        if self.detection_thread is None or not self.detection_thread.is_alive():
            running_flag['running'] = True
            self.detection_thread = threading.Thread(target=self._detection_loop, args=(running_flag,))
            self.detection_thread.start()
        else:
            print("Detection is already running in a separate thread.")

    def check_detections(self):
        """
        Perform a single detection check on the current camera frame.
        
        Captures one frame and checks for target objects. Sends notifications
        for any detected target objects.
        
        Returns:
            list: List of detected objects in the current frame.
            
        Raises:
            Exception: If YOLO has not been initialized.
        """
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
        """
        Send notifications to all configured users about a detected object.
        
        Args:
            detected_object (str): Name of the detected object to notify about.
        """
        for user_id in self.user_settings['user_ids']:
            self.notification_system.notify(user_id, f"{detected_object} detected!")

    def release_camera(self):
        """
        Release the camera resource used by the YOLO detection system.
        
        Should be called when shutting down to properly clean up camera resources.
        """
        if self.yolo is not None:
            self.yolo.release_camera()