#!/usr/bin/env python3
"""
Interactive notification client for receiving detection alerts.

This standalone client connects to the notification system via socket
and displays incoming notifications when objects are detected. Features
an interactive command interface allowing users to start/stop listening
and gracefully exit the application.

The client runs in a separate thread to handle notifications while
maintaining an interactive command prompt for user control.

Usage:
    python notification_client.py
    
Commands:
    start - Begin listening for notifications
    stop  - Stop listening for notifications  
    exit  - Exit the application
    help  - Show available commands
"""

import socket
import threading
import sys

# Flag to control if the listener thread should run
running_flag = {'running': False}
listener_thread = None

def notification_listener(sock):
    """
    Listen for incoming notification connections in a separate thread.
    
    This function runs continuously in a background thread, accepting
    incoming socket connections from the detection system and displaying
    notification messages to the user.
    
    Args:
        sock: The bound socket server instance to listen on.
        
    Note:
        Uses a timeout to allow periodic checking of the running_flag
        for graceful shutdown without blocking indefinitely.
    """
    # Set a timeout on the socket so that the accept() operation doesn't block forever.
    # This allows the while loop to check the running_flag.
    sock.settimeout(1.0) 
    
    while running_flag['running']:
        try:
            conn, addr = sock.accept()
            with conn:
                data = conn.recv(1024) 
                if data:
                    print(f"\nNOTIFICATION: {data.decode()}")
                    # Reprint the prompt after receiving a notification
                    print("Enter command: ", end="", flush=True)
        except socket.timeout:
            # A timeout is expected, it allows the loop to check the flag and continue
            continue
        except Exception as e:
            if running_flag['running']:
                print(f"\nError in listener thread: {e}")
            break
    print("Notification listener stopped.")

def main():
    """
    Main interactive function for the notification client.
    
    Creates a socket server and provides an interactive command interface
    for controlling the notification listener. Users can start/stop the
    listener and exit the application gracefully.
    
    Commands:
        start: Start the notification listener in a background thread
        stop:  Stop the notification listener and wait for thread cleanup
        exit:  Exit the application with proper resource cleanup
        help:  Display available commands
        
    The socket server is created once and reused across start/stop cycles
    to avoid port binding issues.
    """
    global listener_thread
    host = 'localhost'
    port = 65432

    # Create the socket outside the loop so it's available to the thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    
    print("Notification client ready. Type 'start' to begin listening for notifications.")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "start":
            if not running_flag['running']:
                print("Starting notification listener...")
                running_flag['running'] = True
                # Start listening in a new thread
                listener_thread = threading.Thread(target=notification_listener, args=(server_socket,))
                listener_thread.start()
            else:
                print("Listener is already running.")

        elif command == "stop":
            if running_flag['running']:
                print("Stopping notification listener...")
                running_flag['running'] = False
                # Wait for the thread to finish its execution
                if listener_thread:
                    listener_thread.join()
            else:
                print("Listener is not running.")

        elif command == "exit":
            print("Exiting application.")
            if running_flag['running']:
                running_flag['running'] = False
                if listener_thread:
                    listener_thread.join()
            server_socket.close()
            sys.exit(0)
            
        elif command == "help":
            print("Available commands:\n- start: Start listening for notifications\n- stop: Stop listening\n- exit: Exit the application")

        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting application.")
        running_flag['running'] = False
        if listener_thread:
            listener_thread.join()