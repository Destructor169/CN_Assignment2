#!/usr/bin/env python3
import socket
import argparse
import time
import os

def create_client(nagle_enabled):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Disable Nagle's algorithm if specified
    if not nagle_enabled:
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    print(f"Nagle's Algorithm: {'Disabled' if not nagle_enabled else 'Enabled'}")
    
    return client_socket

def send_file(client_socket, file_path, server_address, server_port, rate_bytes_per_sec, duration_secs):
    # Connect to the server
    client_socket.connect((server_address, server_port))
    
    # Read the file
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    file_size = len(file_data)
    print(f"File size: {file_size} bytes")
    
    # Calculate sleep time between sends to achieve desired rate
    bytes_per_send = min(40, file_size)  # Send at most 40 bytes at a time
    sleep_time = 1.0 / (rate_bytes_per_sec / bytes_per_send)
    
    # Send the file
    bytes_sent = 0
    start_time = time.time()
    end_time = start_time + duration_secs
    
    try:
        while time.time() < end_time:
            # Calculate how many bytes to send in this iteration
            remaining = file_size - (bytes_sent % file_size)
            to_send = min(bytes_per_send, remaining)
            
            # Send the data
            offset = bytes_sent % file_size
            client_socket.send(file_data[offset:offset+to_send])
            
            bytes_sent += to_send
            
            # Sleep to maintain the rate
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("Transfer interrupted by user")
    except Exception as e:
        print(f"Error during transfer: {e}")
    
    actual_duration = time.time() - start_time
    
    print(f"Sent {bytes_sent} bytes in {actual_duration:.2f} seconds")
    print(f"Throughput: {(bytes_sent / actual_duration):.2f} bytes/second")
    
    # Close the connection
    client_socket.close()

def main():
    parser = argparse.ArgumentParser(description='TCP Client with configurable Nagle')
    parser.add_argument('--server', type=str, default='localhost', help='Server address')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    parser.add_argument('--file', type=str, required=True, help='File to send')
    parser.add_argument('--nagle', action='store_true', help='Enable Nagle\'s algorithm')
    parser.add_argument('--rate', type=int, default=40, help='Transfer rate in bytes/second')
    parser.add_argument('--duration', type=int, default=120, help='Duration in seconds')
    
    args = parser.parse_args()
    
    client_socket = create_client(args.nagle)
    
    send_file(client_socket, args.file, args.server, args.port, args.rate, args.duration)

if __name__ == "__main__":
    main()
