#!/usr/bin/env python3

# This program will take 2 arguments: "disk|cpu|swap|mem|io" and a threshold. 
# It will run whatever check type is passed in the argument.

import argparse
import sys

# Capture CLI arguments
def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="A multi option metrics and health check"
    )
# Define the check type, 5 choices
    parser.add_argument(
        "check_type",
        choices=["disk", "cpu", "memory", "swap", "io"],
        help="The specific hardware component or metric layer to analyze."
    )

 # Threshold flag that applies to any check
    parser.add_argument(
        "-w", "--warning",
        type=int,
        default=80,
        help="Warning threshold percentage (default: 80 percent)"
    )
    
    return parser.parse_args()

# Function to check local disk space and alert if below threshold
def check_disk_space(warning_threshold: int):
    import shutil

    total, used, free = shutil.disk_usage("/")
    # Change calculation to USED percentage to match CPU/RAM logic consistency
    used_percentage = (used / total) * 100
        
    print(f"Disk space check: {used_percentage:.2f}% used")
    
    if used_percentage > (warning_threshold):
        print(f" ALERT: Disk space is above {warning_threshold}%! Consider cleaning up.")
    else:
        print(" Disk space is sufficient.")


# Function to check local cpu and alert if below threshold
def check_cpu_health(warning_threshold: int):
    import psutil
    cpu_usage = psutil.cpu_percent(interval=1)
    
    print(f"CPU usage check: {cpu_usage:.2f}% used")
    
    if cpu_usage > warning_threshold:
        print(f" ALERT: CPU usage is above {warning_threshold}%! Consider investigating.")
    else:
        print(" CPU usage is within acceptable limits.")

# Function to check local memory and alert if below threshold
def check_memory_health(warning_threshold: int):
    import psutil
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    print(f"Memory usage check: {memory_usage:.2f}% used")
    
    if memory_usage > warning_threshold:
        print(f" ALERT: Memory usage is above {warning_threshold}%! Consider investigating.")
    else:
        print(" Memory usage is within acceptable limits.")

# Function to check local swap and alert if below threshold
def check_swap_health(warning_threshold: int):
    import psutil
    swap = psutil.swap_memory()
    swap_usage = swap.percent

    print(f"Swap usage check: {swap_usage:.2f}% used")

    if swap_usage > warning_threshold:
        print(f" ALERT: Swap usage is above {warning_threshold}%! Consider investigating.")
    else:
        print(" Swap usage is within acceptable limits.")

# Function to check local io and alert if below threshold
def check_io_health(warning_threshold: int):
    import psutil
    io_counters = psutil.disk_io_counters()
    read_bytes = io_counters.read_bytes
    write_bytes = io_counters.write_bytes

    print(f"IO check: Read {read_bytes} bytes, Write {write_bytes} bytes")

    # For IO, we can define a simple threshold based on total bytes read/written
    total_io = read_bytes + write_bytes
    if total_io > warning_threshold * 1e6:  # Convert MB to bytes for comparison
        print(f" ALERT: IO operations exceed {warning_threshold} MB! Consider investigating.")
    else:
        print(" IO operations are within acceptable limits.")   

def main() -> int:
    """Parse command-line arguments and execute the appropriate health check."""        
    args = parse_args() 
# Execute check based on the argument given
    if args.check_type == "disk":
        return check_disk_space(args.warning)
        
    elif args.check_type == "cpu":
        return check_cpu_health(args.warning)
        
    elif args.check_type == "memory":
        return check_memory_health(args.warning)
        
    elif args.check_type == "swap":
        return check_swap_health(args.warning)
        
    elif args.check_type == "io":
        return check_io_health(args.warning)
        
    return 0
   
if __name__ == "__main__":
    raise SystemExit(main())