#  Support Automation Utilities

A collection of lightweight Python scripts designed to automate system administration tasks, monitor server uptime, and parse application logs for rapid incident response.

## Scripts Included

### 1. checkFile.py
* **Purpose:** Checks for the existence of a file in a given directory. Checks if the file is empty or not.

### 2. Log Parser Utility (`findErrors.py`)
* **Purpose:** Scans a target directory for log files and aggregates specific error metrics based on a customizable configuration file (`errors.txt`). Can be tested with applicationLogs.json.

### 3. Start a listener
* **Purpose:** Open a udp or tcp socket on a given port for connectivity testing.

### 4. Server Health Check (`urlHealthCheck.py`)
* **Purpose:** Pings a target URL to verify server responsiveness and records latency data.
