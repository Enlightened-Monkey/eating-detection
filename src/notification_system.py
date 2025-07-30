"""
Notification system module.

This module provides a notification system that supports both callback-based
and socket-based notifications for alerting users about detected objects.
"""

import socket

class NotificationSystem:
    """
    A notification system that supports multiple notification methods.
    
    This class manages user subscriptions and delivers notifications through
    both callback functions and socket connections. It maintains a list of
    subscribers and can send messages to specific users.
    
    Attributes:
        subscribers (dict): Dictionary mapping user IDs to lists of callback functions.
        host (str): Hostname for socket connections.
        port (int): Port number for socket connections.
    """
    def __init__(self, host='localhost', port=65432):
        """
        Initialize the notification system.
        
        Args:
            host (str, optional): Hostname for socket connections. Defaults to 'localhost'.
            port (int, optional): Port number for socket connections. Defaults to 65432.
        """
        self.subscribers = {}
        self.host = host
        self.port = port

    def subscribe(self, user_id, callback):
        """
        Subscribe a user to notifications with a callback function.
        
        Args:
            user_id: Unique identifier for the user.
            callback (callable): Function to call when notifications are sent to this user.
        """
        if user_id not in self.subscribers:
            self.subscribers[user_id] = []
        self.subscribers[user_id].append(callback)

    def unsubscribe(self, user_id, callback):
        """
        Unsubscribe a user's callback from notifications.
        
        Args:
            user_id: Unique identifier for the user.
            callback (callable): The callback function to remove from notifications.
        """
        if user_id in self.subscribers:
            self.subscribers[user_id].remove(callback)

    def notify(self, user_id, message):
        """
        Send a notification to a specific user through all available methods.
        
        Sends the message to all registered callbacks for the user and also
        attempts to send via socket connection to any listening clients.
        
        Args:
            user_id: Unique identifier for the user to notify.
            message (str): The notification message to send.
        """
        if user_id in self.subscribers:
            for callback in self.subscribers[user_id]:
                callback(message)
        # Send to socket client
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(message.encode())
        except Exception as e:
            print(f"Socket notification failed: {e}")

    def event_listener(self, user_id, message):
        """
        Event listener method for triggering notifications.
        
        This method can be used as an event handler that automatically
        sends notifications when called.
        
        Args:
            user_id: Unique identifier for the user to notify.
            message (str): The notification message to send.
        """
        # This method can be used to listen for events and trigger notifications
        self.notify(user_id, message)