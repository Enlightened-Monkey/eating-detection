import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from notification_system import NotificationSystem

@pytest.fixture
def system():
    return NotificationSystem()

def test_subscribe_and_notify_callback(system):
    callback = MagicMock()
    system.subscribe(1, callback)
    system.notify(1, "hello")
    callback.assert_called_once_with("hello")

def test_unsubscribe(system):
    callback = MagicMock()
    system.subscribe(1, callback)
    system.unsubscribe(1, callback)
    system.notify(1, "msg")
    callback.assert_not_called()

def test_notify_socket_success(system):
    with patch('socket.socket') as mock_socket:
        instance = mock_socket.return_value.__enter__.return_value
        system.subscribe(1, lambda x: None)
        system.notify(1, "test message")
        instance.connect.assert_called()
        instance.sendall.assert_called_with(b"test message")

def test_notify_socket_failure(system):
    with patch('socket.socket', side_effect=Exception("fail")):
        system.subscribe(1, lambda x: None)
        # Should print error but not raise
        system.notify(1, "test")

def test_event_listener(system):
    callback = MagicMock()
    system.subscribe(2, callback)
    system.event_listener(2, "event!")
    callback.assert_called_once_with("event!")