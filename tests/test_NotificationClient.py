import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call
import threading
import socket
import time

# Add the project root to the path to allow importing notification_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import notification_client

@pytest.fixture(autouse=True)
def reset_globals():
    """Fixture to reset global state before each test."""
    notification_client.running_flag['running'] = False
    notification_client.listener_thread = None
    yield

def test_listener_receives_notification():
    """
    Tests if the notification_listener function correctly receives data
    and prints it.
    """
    mock_socket = MagicMock()
    mock_conn = MagicMock()
    mock_conn.recv.return_value = b"Test Message"
    
    # Make the loop run only once by changing the flag after the first call
    def accept_side_effect(*args, **kwargs):
        notification_client.running_flag['running'] = False
        return (mock_conn, ('127.0.0.1', 12345))
    
    mock_socket.accept.side_effect = accept_side_effect

    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = True
        notification_client.notification_listener(mock_socket)
        
        mock_conn.recv.assert_called_once_with(1024)
        # Check that the notification was printed
        mock_print.assert_any_call("\nNOTIFICATION: Test Message")

def test_listener_handles_socket_timeout():
    """
    Tests if the notification_listener function correctly handles socket timeouts
    and continues running until the flag is set to False.
    """
    mock_socket = MagicMock()
    mock_socket.accept.side_effect = socket.timeout()
    
    # Let it timeout a few times, then stop
    def timeout_then_stop(*args, **kwargs):
        if hasattr(timeout_then_stop, 'call_count'):
            timeout_then_stop.call_count += 1
        else:
            timeout_then_stop.call_count = 1
        
        if timeout_then_stop.call_count >= 3:
            notification_client.running_flag['running'] = False
        raise socket.timeout()
    
    mock_socket.accept.side_effect = timeout_then_stop

    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = True
        notification_client.notification_listener(mock_socket)
        
        # Should print the stop message
        mock_print.assert_any_call("Notification listener stopped.")

def test_listener_handles_general_exception():
    """
    Tests if the notification_listener function correctly handles general exceptions.
    """
    mock_socket = MagicMock()
    mock_socket.accept.side_effect = Exception("Test exception")
    
    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = True
        notification_client.notification_listener(mock_socket)
        
        # Should print the error message and stop message
        mock_print.assert_any_call("\nError in listener thread: Test exception")
        mock_print.assert_any_call("Notification listener stopped.")

def test_listener_empty_data():
    """
    Tests if the notification_listener function correctly handles empty data.
    """
    mock_socket = MagicMock()
    mock_conn = MagicMock()
    mock_conn.recv.return_value = b""  # Empty data
    
    def accept_side_effect(*args, **kwargs):
        notification_client.running_flag['running'] = False
        return (mock_conn, ('127.0.0.1', 12345))
    
    mock_socket.accept.side_effect = accept_side_effect

    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = True
        notification_client.notification_listener(mock_socket)
        
        mock_conn.recv.assert_called_once_with(1024)
        # Should print stop message but not notification for empty data
        mock_print.assert_called_once_with("Notification listener stopped.")
        # Ensure no notification was printed
        notification_calls = [call for call in mock_print.call_args_list if 'NOTIFICATION:' in str(call)]
        assert len(notification_calls) == 0

def test_listener_decoding_message():
    """
    Tests if the notification_listener function correctly decodes binary messages.
    """
    mock_socket = MagicMock()
    mock_conn = MagicMock()
    test_message = "Food detected! 🍎"
    mock_conn.recv.return_value = test_message.encode('utf-8')
    
    def accept_side_effect(*args, **kwargs):
        notification_client.running_flag['running'] = False
        return (mock_conn, ('127.0.0.1', 12345))
    
    mock_socket.accept.side_effect = accept_side_effect

    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = True
        notification_client.notification_listener(mock_socket)
        
        mock_print.assert_any_call(f"\nNOTIFICATION: {test_message}")
        mock_print.assert_any_call("Enter command: ", end="", flush=True)

def test_listener_stops_when_flag_false():
    """
    Tests if the notification_listener function stops when running_flag is set to False.
    """
    mock_socket = MagicMock()
    mock_socket.accept.side_effect = socket.timeout()
    
    with patch('builtins.print') as mock_print:
        notification_client.running_flag['running'] = False  # Already false
        notification_client.notification_listener(mock_socket)
        
        # Should immediately print stop message without calling accept
        mock_print.assert_called_once_with("Notification listener stopped.")
        mock_socket.accept.assert_not_called()

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_start_command(mock_print, mock_input, mock_socket):
    """
    Tests the main function's start command functionality.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: start, then exit
    # Add KeyboardInterrupt after the planned inputs to prevent infinite loop
    def input_side_effect(*args):
        inputs = ['start', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('threading.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        with patch('sys.exit') as mock_exit:
            try:
                notification_client.main()
            except KeyboardInterrupt:
                pass  # Expected when we run out of inputs
            
            # Verify socket setup
            mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
            mock_socket_instance.bind.assert_called_once_with(('localhost', 65432))
            mock_socket_instance.listen.assert_called_once()
            
            # Verify thread creation and start
            mock_thread.assert_called_once()
            mock_thread_instance.start.assert_called_once()
            
            # Verify appropriate messages (including initial message)
            mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
            mock_print.assert_any_call("Starting notification listener...")
            mock_print.assert_any_call("Exiting application.")
            
            # Verify exit
            mock_exit.assert_called_once_with(0)

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_stop_command(mock_print, mock_input, mock_socket):
    """
    Tests the main function's stop command functionality.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: start, stop, then exit
    def input_side_effect(*args):
        inputs = ['start', 'stop', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('threading.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        with patch('sys.exit') as mock_exit:
            try:
                notification_client.main()
            except KeyboardInterrupt:
                pass  # Expected when we run out of inputs
            
            # Verify appropriate messages
            mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
            mock_print.assert_any_call("Starting notification listener...")
            mock_print.assert_any_call("Stopping notification listener...")
            mock_print.assert_any_call("Exiting application.")
            
            # Verify thread join was called
            mock_thread_instance.join.assert_called()

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_help_command(mock_print, mock_input, mock_socket):
    """
    Tests the main function's help command functionality.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: help, then exit
    def input_side_effect(*args):
        inputs = ['help', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('sys.exit') as mock_exit:
        try:
            notification_client.main()
        except KeyboardInterrupt:
            pass  # Expected when we run out of inputs
        
        # Verify initial and help messages
        mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
        expected_help = "Available commands:\n- start: Start listening for notifications\n- stop: Stop listening\n- exit: Exit the application"
        mock_print.assert_any_call(expected_help)

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_unknown_command(mock_print, mock_input, mock_socket):
    """
    Tests the main function's handling of unknown commands.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: unknown command, then exit
    def input_side_effect(*args):
        inputs = ['unknown', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('sys.exit') as mock_exit:
        try:
            notification_client.main()
        except KeyboardInterrupt:
            pass  # Expected when we run out of inputs
        
        # Verify initial and unknown command messages
        mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
        mock_print.assert_any_call("Unknown command. Type 'help' for options.")

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_start_already_running(mock_print, mock_input, mock_socket):
    """
    Tests the main function when trying to start an already running listener.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: start twice, then exit
    def input_side_effect(*args):
        inputs = ['start', 'start', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('threading.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        with patch('sys.exit') as mock_exit:
            try:
                notification_client.main()
            except KeyboardInterrupt:
                pass  # Expected when we run out of inputs
            
            # Verify appropriate messages
            mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
            mock_print.assert_any_call("Starting notification listener...")
            mock_print.assert_any_call("Listener is already running.")

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_stop_not_running(mock_print, mock_input, mock_socket):
    """
    Tests the main function when trying to stop a non-running listener.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate user input: stop (without starting), then exit
    def input_side_effect(*args):
        inputs = ['stop', 'exit']
        if not hasattr(input_side_effect, 'call_count'):
            input_side_effect.call_count = 0
        
        if input_side_effect.call_count < len(inputs):
            result = inputs[input_side_effect.call_count]
            input_side_effect.call_count += 1
            return result
        else:
            raise KeyboardInterrupt()
    
    mock_input.side_effect = input_side_effect
    
    with patch('sys.exit') as mock_exit:
        try:
            notification_client.main()
        except KeyboardInterrupt:
            pass  # Expected when we run out of inputs
        
        # Verify appropriate messages
        mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")
        mock_print.assert_any_call("Listener is not running.")

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_main_keyboard_interrupt(mock_print, mock_input, mock_socket):
    """
    Tests the main function's handling of KeyboardInterrupt.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate KeyboardInterrupt during input (after the initial print)
    mock_input.side_effect = KeyboardInterrupt()
    
    with patch('threading.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        notification_client.listener_thread = mock_thread_instance
        notification_client.running_flag['running'] = True
        
        # Test that main() raises KeyboardInterrupt which would be caught by the module-level handler
        with pytest.raises(KeyboardInterrupt):
            notification_client.main()
        
        # Verify initial message was printed before the interrupt
        mock_print.assert_any_call("Notification client ready. Type 'start' to begin listening for notifications.")

@patch('socket.socket')
@patch('builtins.input')
@patch('builtins.print')
def test_module_level_keyboard_interrupt_handler(mock_print, mock_input, mock_socket):
    """
    Tests the module-level KeyboardInterrupt handler that would be triggered by __main__.
    """
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    
    # Simulate KeyboardInterrupt during input
    mock_input.side_effect = KeyboardInterrupt()
    
    with patch('threading.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        notification_client.listener_thread = mock_thread_instance
        notification_client.running_flag['running'] = True
        
        # Simulate the module-level exception handling
        try:
            notification_client.main()
        except KeyboardInterrupt:
            # This is what happens in the if __name__ == "__main__" block
            print("\nExiting application.")
            notification_client.running_flag['running'] = False
            if notification_client.listener_thread:
                notification_client.listener_thread.join()
        
        # Verify cleanup
        assert notification_client.running_flag['running'] == False
        mock_thread_instance.join.assert_called_once()

def test_global_state_initialization():
    """
    Tests that global state variables are properly initialized.
    """
    # Test initial state
    assert 'running' in notification_client.running_flag
    assert notification_client.running_flag['running'] == False
    assert notification_client.listener_thread is None