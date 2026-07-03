# This script will take a URL as an argument and check the health of the URL by
# sending an HTTP request and analyzing the response.

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

