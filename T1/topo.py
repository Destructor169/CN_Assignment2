#!/usr/bin/env python3
import socket
import argparse
import time
import os

def create_server(port, nagle_enabled, delayed_ack_enabled):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket options
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Disable Nagle's algorithm if specified
    if not nagle_enabled:
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    # Bind the socket to the address
    server_socket.bind(('0.0.0.0', port))
    
    # Start listening
    server_socket.listen(5)
    
    print(f"Server started on port {port}")
    print(f"Nagle's Algorithm: {'Disabled' if not nagle_enabled else 'Enabled'}")
    print(f"Delayed ACK: {'Disabled' if not delayed_ack_enabled else 'Enabled'}")
    
    # If delayed ACK is disabled, set TCP_QUICKACK (Linux-specific)
    if not delayed_ack_enabled:
        # This needs to be done after connection is established
        print("Note: Delayed ACK will be disabled after connection is established")
    
    return server_socket

def handle_client(client_socket, delayed_ack_enabled):
    # If delayed ACK is disabled, set TCP_QUICKACK
    if not delayed_ack_enabled:
        try:
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            print("Disabled Delayed ACK for this connection")
        except AttributeError:
            print("TCP_QUICKACK not supported on this system")
    
    # Receive data from client
    total_bytes = 0
    start_time = time.time()
    
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            total_bytes += len(data)
    except Exception as e:
        print(f"Error receiving data: {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Received {total_bytes} bytes in {duration:.2f} seconds")
    print(f"Throughput: {(total_bytes / duration):.2f} bytes/second")
    
    client_socket.close()

def main():
    parser = argparse.ArgumentParser(description='TCP Server with configurable Nagle and Delayed ACK')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('--nagle', action='store_true', help='Enable Nagle\'s algorithm')
    parser.add_argument('--delayed-ack', action='store_true', help='Enable Delayed ACK')
    
    args = parser.parse_args()
    
    server_socket = create_server(args.port, args.nagle, args.delayed_ack)
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket, args.delayed_ack)
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
