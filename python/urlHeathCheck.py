#!/usr/bin/env python3
"""
System Utility: Start a listener for connectivity testing
Author:         Jason Phaneuf
Created:        July 2026
GitHub:         ://github.com/mrjasonphaneuf/support-tools/python/startListener.py

Description:
    This script will take two arguments- -p port -t "tcp or udp". It will 
    open a local port, wait for a connection, and print connection details once
    a remote connection is made. It will then close the connection.will take a 
    directory path and a filename as an argument. It will then check the 
    existence of that directory, then check for the file's existence and whether
    it is a zero byte file.

Usage:
    python startListener.py -p port -t tcp
""" 

import urllib.request
import time
import sys

def main(url):
 # If the user forgot to type http:// or https://, fix it automatically
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"Checking status for: {url}...")
    try:
        start_time = time.time()
        # Open the URL and get the response code
        response = urllib.request.urlopen(url, timeout=5)
        response_time = time.time() - start_time
        
        if response.getcode() == 200:
            print(f" SUCCESS: Server is UP! (Response time: {response_time:.2f} seconds)")
        else:
            print(f" WARNING: Server returned status code {response.getcode()}")
            
    except Exception as e:
        print(f" ERROR: Server is DOWN or unreachable. Details: {e}")

if __name__ == "__main__":
    # Check arguments before passing them to any functions
    if len(sys.argv) != 2:
        print("Usage: python urlHealthCheck.py <URL>")
        sys.exit(1) 

# Test the health check function

main(sys.argv[1])    

