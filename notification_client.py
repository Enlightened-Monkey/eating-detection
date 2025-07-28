#!/usr/bin/env python3
import socket

def main():
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