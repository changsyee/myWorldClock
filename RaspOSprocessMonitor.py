import os
import psutil
import time
import threading

def set_high_priority():
    """Sets the process to a high priority (lower nice value)."""
    try:
        # -10 is high priority. Range is -20 (max) to 19 (min).
        # Note: Increasing priority (negative values) usually requires sudo.
        os.nice(-10)
        print("Successfully set priority to -10")
    except PermissionError:
        print("Permission Denied: Run with 'sudo' to increase priority.")

def resource_monitor(interval=5):
    """Background thread to monitor CPU and RAM usage."""
    process = psutil.Process(os.getpid())
    print(f"{'Time':<10} | {'CPU %':<8} | {'RAM (MB)':<10}")
    print("-" * 35)
    
    while True:
        cpu_pct = process.cpu_percent(interval=1)
        ram_mb = process.memory_info().rss / (1024 * 1024)
        print(f"{time.strftime('%H:%M:%S'):<10} | {cpu_pct:<8.1f} | {ram_mb:<10.2f}")
        time.sleep(interval)

# --- Start the program ---
# 1. Boost Priority
set_high_priority()

# 2. Start the monitor in a separate thread so it doesn't block your code
monitor_thread = threading.Thread(target=resource_monitor, daemon=True)
monitor_thread.start()

# 3. Your main Raspberry Pi logic goes here
print("Starting main loop...")
while True:
    # Simulating your work
    time.sleep(1)