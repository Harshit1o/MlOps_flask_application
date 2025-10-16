"""
Load testing script to trigger HPA autoscaling
"""
import requests
import threading
import time
from datetime import datetime

# Configuration
URL = "http://localhost:5000/predict"
DURATION = 120  # seconds
CONCURRENT_REQUESTS = 50
REQUEST_DELAY = 0.01  # seconds between requests

# Sample prediction data
payload = {
    "features": [5.1, 3.5, 1.4, 0.2]
}

success_count = 0
error_count = 0
stop_flag = False

def make_request():
    """Make a single prediction request"""
    global success_count, error_count
    try:
        response = requests.post(URL, json=payload, timeout=5)
        if response.status_code == 200:
            success_count += 1
        else:
            error_count += 1
    except Exception as e:
        error_count += 1

def worker():
    """Worker thread to continuously make requests"""
    while not stop_flag:
        make_request()
        time.sleep(REQUEST_DELAY)

def print_stats():
    """Print statistics every 5 seconds"""
    start_time = time.time()
    while not stop_flag:
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Elapsed: {int(elapsed)}s | "
              f"Success: {success_count} | "
              f"Errors: {error_count} | "
              f"Rate: {success_count/elapsed:.1f} req/s")
        time.sleep(5)

if __name__ == "__main__":
    print(f"Starting load test...")
    print(f"URL: {URL}")
    print(f"Duration: {DURATION} seconds")
    print(f"Concurrent workers: {CONCURRENT_REQUESTS}")
    print(f"\nIn another terminal, run:")
    print(f"  kubectl get hpa -w")
    print(f"\nStarting in 3 seconds...\n")
    time.sleep(3)

    # Start worker threads
    threads = []
    for i in range(CONCURRENT_REQUESTS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    # Start stats printer
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()

    # Run for specified duration
    try:
        time.sleep(DURATION)
    except KeyboardInterrupt:
        print("\n\nStopping load test...")
    
    stop_flag = True
    time.sleep(1)

    # Final stats
    print(f"\n{'='*60}")
    print(f"Load test completed!")
    print(f"Total successful requests: {success_count}")
    print(f"Total errors: {error_count}")
    print(f"Average rate: {success_count/DURATION:.1f} requests/second")
    print(f"{'='*60}")
    print(f"\nCheck HPA status:")
    print(f"  kubectl get hpa")
    print(f"  kubectl get pods")
