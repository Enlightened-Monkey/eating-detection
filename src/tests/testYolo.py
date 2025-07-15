import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from yolo import YOLO

@pytest.fixture
def yolo():
    # Mockujemy model UltralyticsYOLO
    with patch('yolo.UltralyticsYOLO') as MockModel:
        mock_model = MockModel.return_value
        mock_model.names = {0: 'bottle', 1: 'apple'}
        return YOLO(camera_index=0, resolution=(640, 480), frame_check_interval=1, model_path='fake.pt', threshold=0.5)

def test_initialize_camera_success(yolo):
    with patch('cv2.VideoCapture') as mock_capture:
        mock_instance = mock_capture.return_value
        mock_instance.isOpened.return_value = True
        yolo.initialize_camera()
        mock_capture.assert_called_once_with(0)
        mock_instance.set.assert_any_call(3, 640)
        mock_instance.set.assert_any_call(4, 480)

def test_initialize_camera_failure(yolo):
    with patch('cv2.VideoCapture') as mock_capture:
        mock_instance = mock_capture.return_value
        mock_instance.isOpened.return_value = False
        with pytest.raises(RuntimeError, match="Error: Could not open webcam."):
            yolo.initialize_camera()

def test_capture_image_success(yolo):
    yolo.camera = MagicMock()
    yolo.camera.read.return_value = (True, 'frame')
    frame = yolo.capture_image()
    assert frame == 'frame'

def test_capture_image_none(yolo):
    yolo.camera = MagicMock()
    yolo.camera.read.return_value = (False, None)
    frame = yolo.capture_image()
    assert frame is None

def test_detect_objects_success(yolo):
    # Mockujemy wynik modelu
    mock_result = MagicMock()
    mock_box = MagicMock()
    mock_box.cls = [0]
    mock_box.conf = [0.8]
    mock_result.boxes = [mock_box]
    yolo.model = MagicMock(return_value=[mock_result])
    yolo.model.names = {0: 'bottle'}
    detected = yolo.detect_objects('frame')
    assert detected == ['bottle']

def test_detect_objects_below_threshold(yolo):
    mock_result = MagicMock()
    mock_box = MagicMock()
    mock_box.cls = [1]
    mock_box.conf = [0.3]
    mock_result.boxes = [mock_box]
    yolo.model = MagicMock(return_value=[mock_result])
    yolo.model.names = {1: 'apple'}
    detected = yolo.detect_objects('frame')
    assert detected == []

def test_detect_objects_exception(yolo):
    yolo.model = MagicMock(side_effect=Exception("fail"))
    detected = yolo.detect_objects('frame')
    assert detected == []

def test_release_camera(yolo):
    yolo.camera = MagicMock()
    yolo.release_camera()
    yolo.camera.release.assert_called_once()
    assert yolo.camera is None

def test_get_detected_objects(yolo):
    yolo.detected_objects = ['bottle', 'apple']
    assert yolo.get_detected_objects() == ['bottle', 'apple']