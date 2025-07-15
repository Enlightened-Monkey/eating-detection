import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from food_detection_system import FoodDetectionSystem

@pytest.fixture
def user_settings():
    return {
        'objects_to_detect': ['bottle', 'apple'],
        'threshold': 0.5,
        'camera_settings': {
            'resolution': [640, 480],
            'frame_check_interval': 1.0
        },
        'user_ids': [1, 2]
    }

@pytest.fixture
def notification_system():
    return MagicMock()

@pytest.fixture
def food_system(user_settings, notification_system):
    return FoodDetectionSystem(user_settings, notification_system)

def test_initialize_yolo_success(food_system):
    with patch('food_detection_system.YOLO') as MockYOLO:
        mock_yolo = MockYOLO.return_value
        mock_yolo.initialize_camera.return_value = None
        food_system.initialize_yolo()
        assert food_system.yolo is mock_yolo
        mock_yolo.initialize_camera.assert_called_once()

def test_initialize_yolo_failure(food_system):
    with patch('food_detection_system.YOLO', side_effect=Exception("fail")):
        with pytest.raises(RuntimeError, match="Failed to initialize YOLO: fail"):
            food_system.initialize_yolo()

def test_check_detections_detected(food_system):
    food_system.yolo = MagicMock()
    food_system.yolo.capture_image.return_value = 'frame'
    food_system.yolo.detect_objects.return_value = ['bottle', 'banana']
    food_system.user_settings['objects_to_detect'] = ['bottle']
    food_system.user_settings['user_ids'] = [1]
    food_system.notification_system.notify = MagicMock()
    detected = food_system.check_detections()
    assert detected == ['bottle', 'banana']
    food_system.notification_system.notify.assert_called_once_with(1, "bottle detected!")

def test_check_detections_none(food_system):
    food_system.yolo = MagicMock()
    food_system.yolo.capture_image.return_value = None
    detected = food_system.check_detections()
    assert detected == []

def test_check_detections_yolo_not_initialized(food_system):
    food_system.yolo = None
    with pytest.raises(Exception, match="YOLO has not been initialized."):
        food_system.check_detections()

def test_notify_users(food_system):
    food_system.notification_system.notify = MagicMock()
    food_system.user_settings['user_ids'] = [1, 2]
    food_system.notify_users('apple')
    food_system.notification_system.notify.assert_any_call(1, "apple detected!")
    food_system.notification_system.notify.assert_any_call(2, "apple detected!")

def test_release_camera(food_system):
    food_system.yolo = MagicMock()
    food_system.release_camera()
    food_system.yolo.release_camera.assert_called_once()