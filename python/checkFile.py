#!/usr/bin/env python3
"""
System Utility: Check for a file's existence in a given directory
Author:         Jason Phaneuf
Created:        July 2026
GitHub:         ://github.com/mrjasonphaneuf/support-tools

Description:
    This script will take a directory path and a filename as an argument. It 
    will then check the existence of that directory, then check for the file's
    existence and whether it is a zero byte file.

Usage:
    python checkFile.py -d myDir -f myFilename
    Example: python multiHealthCheck.py -d logs -f application.log
""" 

#This script will take a directory path and a filename as an argument.
# It will then check the existence of that directory, then check for the 
# file's existence and whether it is a zero byte file.

import os
import sys  

def main():
# 1. Capture the two command line arguments: -d myDir -f myFilename
    if len(sys.argv) != 5:
        print("Usage: python checkFile.py -d <directory> -f <filename>")
        sys.exit(1) 

# 2. Check that the directory exists, if it doesn't, print an error
    if sys.argv[1] != "-d":
        print("Error: Missing -d argument for directory")
        sys.exit(1) 

# 2a. If the directory argument isn't given, exit with a help explanation of how to run the script
    if not os.path.isdir(sys.argv[2]):
        print(f"Error: Directory '{sys.argv[2]}' does not exist.")
        sys.exit(1)

# 3. Check that the file exists and is not empty.
    if sys.argv[3] != "-f":
        print("Error: Missing -f argument for filename")
        sys.exit(1)

    file_path = os.path.join(sys.argv[2], sys.argv[4])
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    if os.path.getsize(file_path) == 0:
        print(f"Error: File '{file_path}' is empty.")
        sys.exit(1)

# 4. If the file exists and has data in it, print success
    print(f"Success: File '{file_path}' exists and is not empty.")

if __name__ == "__main__":
    raise SystemExit(main())