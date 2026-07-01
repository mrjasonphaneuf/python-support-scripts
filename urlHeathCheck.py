import urllib.request
import time

def check_server_health(url):
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

# Test the health check function
check_server_health("https://google.com")

# Function to check local disk space and alert if below 10%
def check_disk_space():
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_percentage = (free / total) * 100
    
    print(f"Disk space check: {free_percentage:.2f}% free")
    
    if free_percentage < 10:
        print(" ALERT: Disk space is below 10%! Consider cleaning up.")
    else:
        print(" Disk space is sufficient.")
check_disk_space()