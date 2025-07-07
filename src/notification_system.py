import socket

class NotificationSystem:
    def __init__(self, host='localhost', port=65432):
        self.subscribers = {}
        self.host = host
        self.port = port

    def subscribe(self, user_id, callback):
        if user_id not in self.subscribers:
            self.subscribers[user_id] = []
        self.subscribers[user_id].append(callback)

    def unsubscribe(self, user_id, callback):
        if user_id in self.subscribers:
            self.subscribers[user_id].remove(callback)

    def notify(self, user_id, message):
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
        # This method can be used to listen for events and trigger notifications
        self.notify(user_id, message)