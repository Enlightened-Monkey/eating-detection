#!/usr/bin/env python3
"""
Notification client for receiving detection alerts.

This standalone client connects to the notification system via socket
and displays incoming notifications when objects are detected. Run this
in a separate terminal to receive real-time alerts.
"""

import socket

def main():
    """
    Main function for the notification client.
    
    Creates a socket server that listens for incoming notification messages
    from the detection system and displays them to the user.
    """
    host = 'localhost'
    port = 65432
    bytesize = 1024  # Buffer size for receiving data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Notification client started. Waiting for notifications...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(bytesize) 
                if data:
                    print(f"\nNOTIFICATION: {data.decode()}")

if __name__ == "__main__":
    main()