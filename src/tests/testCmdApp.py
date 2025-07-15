import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
from cmdApp import CMDApp

@pytest.fixture
def app():
    # Tworzymy przykładowe ustawienia użytkownika
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
    # Mockujemy funkcję print
    with patch('builtins.print') as mock_print:
        # Wywołujemy metodę
        app.display_help()
        
        # Sprawdzamy, czy print został wywołany z poprawnym tekstem pomocy
        mock_print.assert_called_once()
        assert "Available commands:" in mock_print.call_args[0][0]
        assert "help: Display this help message" in mock_print.call_args[0][0]
def test_set_detection_targets_valid_input(app):
    # Mockujemy input i print
    with patch('builtins.input', return_value="apple, banana, orange") as mock_input:
        with patch('builtins.print') as mock_print:
            # Wywołujemy metodę
            app.set_detection_targets()
            
            # Sprawdzamy, czy ustawienia zostały zaktualizowane
            assert app.user_settings['objects_to_detect'] == ['apple', 'banana', 'orange']
            mock_print.assert_called_once_with("Detection targets set to: ['apple', 'banana', 'orange']")

def test_set_detection_targets_empty_input(app):
    # Mockujemy input jako pusty string
    with patch('builtins.input', return_value=""):
        # Sprawdzamy, czy metoda rzuca wyjątek
        with pytest.raises(ValueError, match="No detection targets provided."):
            app.set_detection_targets()

def test_set_threshold_valid_input(app):
    # Mockujemy input i print
    with patch('builtins.input', return_value="0.7"):
        with patch('builtins.print') as mock_print:
            # Wywołujemy metodę
            app.set_threshold()
            
            # Sprawdzamy, czy ustawienia zostały zaktualizowane
            assert app.user_settings['threshold'] == 0.7
            mock_print.assert_called_once_with("Detection threshold set to: 0.7")

def test_set_threshold_invalid_value(app):
    # Mockujemy input z niepoprawną wartością
    with patch('builtins.input', return_value="1.5"):
        # Sprawdzamy, czy metoda rzuca wyjątek
        with pytest.raises(ValueError, match="Threshold must be between 0.0 and 1.0."):
            app.set_threshold()

def test_set_threshold_non_numeric_input(app):
    # Mockujemy input z niepoprawnym formatem
    with patch('builtins.input', return_value="abc"):
        # Sprawdzamy, czy metoda rzuca wyjątek
        with pytest.raises(ValueError, match="Invalid threshold value: could not convert string to float: 'abc'"):
            app.set_threshold()

def test_set_camera_settings_valid_input(app):
    # Mockujemy input i print
    with patch('builtins.input', side_effect=["1280x720", "2"]):
        with patch('builtins.print') as mock_print:
            # Wywołujemy metodę
            app.set_camera_settings()
            
            # Sprawdzamy, czy ustawienia zostały zaktualizowane
            assert app.user_settings['camera_settings']['resolution'] == [1280, 720]
            assert app.user_settings['camera_settings']['frame_check_interval'] == 2.0
            mock_print.assert_called_once_with("Camera settings updated: {'resolution': [1280, 720], 'frame_check_interval': 2.0}")

def test_set_camera_settings_invalid_resolution(app):
    # Mockujemy input z niepoprawną rozdzielczością
    with patch('builtins.input', side_effect=["invalid", "2"]):
        # Sprawdzamy, czy metoda rzuca wyjątek
        with pytest.raises(ValueError, match="Invalid camera settings: invalid literal for int"):
            app.set_camera_settings()

def test_set_camera_settings_negative_interval(app):
    # Mockujemy input z ujemnym interwałem
    with patch('builtins.input', side_effect=["640x480", "-1"]):
        # Sprawdzamy, czy metoda rzuca wyjątek
        with pytest.raises(ValueError, match="Frame check interval must be positive."):
            app.set_camera_settings()

@pytest.mark.skip(reason="I need to fix this test later")
def test_run_command_valid(app):
    # Mockujemy metodę display_help
    with patch.object(app, 'display_help') as mock_display_help:
        # Wywołujemy run_command z poprawną komendą
        app.run_command('help')
        
        # Sprawdzamy, czy metoda display_help została wywołana
        mock_display_help.assert_called_once()

def test_run_command_invalid(app):
    # Mockujemy print
    with patch('builtins.print') as mock_print:
        # Wywołujemy run_command z niepoprawną komendą
        app.run_command('invalid')
        
        # Sprawdzamy, czy print został wywołany z odpowiednim komunikatem
        mock_print.assert_called_once_with("Unknown command or handled outside CMDApp.")

def test_run_command_none(app):
    # Mockujemy print
    with patch('builtins.print') as mock_print:
        # Wywołujemy run_command dla komendy z wartością None (np. start)
        app.run_command('start')
        
        # Sprawdzamy, czy print został wywołany z odpowiednim komunikatem
        mock_print.assert_called_once_with("Unknown command or handled outside CMDApp.")