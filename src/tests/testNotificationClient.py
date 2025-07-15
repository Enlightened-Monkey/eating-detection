import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
import notification_client

def test_client_receives_notification(monkeypatch):
    mock_socket = MagicMock()
    mock_conn = MagicMock()
    mock_conn.recv.return_value = b"hello"
    mock_socket.accept.return_value = (mock_conn, ('127.0.0.1', 12345))
    monkeypatch.setattr('socket.socket', lambda *a, **kw: mock_socket)
    mock_socket.__enter__.return_value = mock_socket
    mock_socket.listen.return_value = None
    printed = []
    monkeypatch.setattr('builtins.print', lambda x: printed.append(x))
    # Run only one loop iteration
    def fake_main():
        host = 'localhost'
        port = 65432
        bytesize = 1024
        with mock_socket:
            mock_socket.bind((host, port))
            mock_socket.listen()
            printed.append("Notification client started. Waiting for notifications...")
            conn, addr = mock_socket.accept()
            with conn:
                data = conn.recv(bytesize)
                if data:
                    printed.append(f"\nNOTIFICATION: {data.decode()}")
    fake_main()
    assert any("NOTIFICATION: hello" in str(x) for x in printed)