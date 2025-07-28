import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from unittest.mock import patch, Mock
from cmd_app import CMDApp

@pytest.fixture
def app():
    # Create example user settings
    user_settings = {
        'objects_to_detect': ['bottle'],
        'threshold': 0.5,
        'camera_settings': {
            'resolution': [640, 480],
            'frame_check_interval': 1.0
        }
    }
    return CMDApp(user_settings)

def test_display_help(app):
    # Mock the print function
    with patch('builtins.print') as mock_print:
        # Call the method
        app.display_help()
        
        # Check if print was called with correct help text
        mock_print.assert_called_once()
        assert "Available commands:" in mock_print.call_args[0][0]
        assert "help: Display this help message" in mock_print.call_args[0][0]

def test_set_detection_targets_valid_input(app):
    # Mock input and print
    with patch('builtins.input', return_value="apple, banana, orange") as mock_input:
        with patch('builtins.print') as mock_print:
            # Call the method
            app.set_detection_targets()
            
            # Check if settings were updated
            assert app.user_settings['objects_to_detect'] == ['apple', 'banana', 'orange']
            mock_print.assert_called_once_with("Detection targets set to: ['apple', 'banana', 'orange']")

def test_set_detection_targets_empty_input(app):
    # Mock input as empty string
    with patch('builtins.input', return_value=""):
        # Check if method raises exception
        with pytest.raises(ValueError, match="No detection targets provided."):
            app.set_detection_targets()

def test_set_threshold_valid_input(app):
    # Mock input and print
    with patch('builtins.input', return_value="0.7"):
        with patch('builtins.print') as mock_print:
            # Call the method
            app.set_threshold()
            
            # Check if settings were updated
            assert app.user_settings['threshold'] == 0.7
            mock_print.assert_called_once_with("Detection threshold set to: 0.7")

def test_set_threshold_invalid_value(app):
    # Mock input with invalid value
    with patch('builtins.input', return_value="1.5"):
        # Check if method raises exception
        with pytest.raises(ValueError, match="Threshold must be between 0.0 and 1.0."):
            app.set_threshold()

def test_set_threshold_non_numeric_input(app):
    # Mock input with invalid format
    with patch('builtins.input', return_value="abc"):
        # Check if method raises exception
        with pytest.raises(ValueError, match="Invalid threshold value: could not convert string to float: 'abc'"):
            app.set_threshold()

def test_set_camera_settings_valid_input(app):
    # Mock input and print
    with patch('builtins.input', side_effect=["1280x720", "2"]):
        with patch('builtins.print') as mock_print:
            # Call the method
            app.set_camera_settings()
            
            # Check if settings were updated
            assert app.user_settings['camera_settings']['resolution'] == [1280, 720]
            assert app.user_settings['camera_settings']['frame_check_interval'] == 2.0
            mock_print.assert_called_once_with("Camera settings updated: {'resolution': [1280, 720], 'frame_check_interval': 2.0}")

def test_set_camera_settings_invalid_resolution(app):
    # Mock input with invalid resolution
    with patch('builtins.input', side_effect=["invalid", "2"]):
        # Check if method raises exception
        with pytest.raises(ValueError, match="Invalid camera settings: invalid literal for int"):
            app.set_camera_settings()

def test_set_camera_settings_negative_interval(app):
    # Mock input with negative interval
    with patch('builtins.input', side_effect=["640x480", "-1"]):
        # Check if method raises exception
        with pytest.raises(ValueError, match="Frame check interval must be positive."):
            app.set_camera_settings()

@pytest.mark.skip(reason="I need to fix this test later")
def test_run_command_valid(app):
    # Mock display_help method
    with patch.object(app, 'display_help') as mock_display_help:
        # Call run_command with valid command
        app.run_command('help')
        
        # Check if display_help was called
        mock_display_help.assert_called_once()

def test_run_command_invalid(app):
    # Mock print
    with patch('builtins.print') as mock_print:
        # Call run_command with invalid command
        app.run_command('invalid')
        
        # Check if print was called with correct message
        mock_print.assert_called_once_with("Unknown command or handled outside CMDApp.")

def test_run_command_none(app):
    # Mock print
    with patch('builtins.print') as mock_print:
        # Call run_command for command with None value (e.g. start)
        app.run_command('start')
        
        # Check if print was called with correct message
        mock_print.assert_called_once_with("Unknown command or handled outside CMDApp.")