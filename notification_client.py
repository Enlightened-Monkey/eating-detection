#!/usr/bin/env python3
import socket
import threading
import sys

# Flag to control if the listener thread should run
running_flag = {'running': False}
listener_thread = None

def notification_listener(sock):
    """
    This function runs in a separate thread and listens for incoming connections.
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