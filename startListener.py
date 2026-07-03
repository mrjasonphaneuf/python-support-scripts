# This program will take two arguments- -p port -t "tcp or udp". It will 
# open a local port, wait for a connection, and print connection details once
# a remote connection is made. It will then close the connection.

import sys
import socket

# 1. Capture the arguments to determine whether a UDP or TCP connection will be used.

def main():
    if len(sys.argv) != 5:
        print("Usage: python startListener.py -p <port> -t <tcp|udp>")
        sys.exit(1)     
    
    server_port = int(sys.argv[2])
    protocol = sys.argv[4]

    if protocol not in ["tcp", "udp"]:
        print("Usage: python startListener.py -p <port> -t <tcp|udp>")
        sys.exit(1)

# 2. Open the socket
    try:
        if protocol == "tcp":
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    
        if protocol == "udp":
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    
# 3. Allow immediate reuse of the port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     
    
# 4. Bind the socket to all available interfaces on the specified port
        server_socket.bind(('', server_port))   

# 5. Wait for the remote connection and print connection details - 
#    remote port and remote IP once a connection is made
        if protocol == "tcp":   
            server_socket.listen(1)   
            print(f"Listening for TCP connections on port {server_port}...")
            conn, addr = server_socket.accept()   
            print(f"Connection established with {addr[0]}:{addr[1]}")
            conn.close()

        if protocol == "udp":
            print(f"Listening for UDP packets on port {server_port}...")
            data, addr = server_socket.recvfrom(1024)
            print(f"UDP packet received from {addr[0]}:{addr[1]}")      

# 7. Add some error handling to catch exceptions and print an error message if the connection fails or if the port is already in use.
    except socket.error as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("Interrupted by user.")   
     
    # 6. Close the connection and clean up
    finally:
        server_socket.close()   
        print("Connection closed.")  

if __name__ == "__main__": 
    main()