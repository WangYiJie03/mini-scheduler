import time
import socket
import requests

MASTER_BASE_URL = "http://127.0.0.1:8000"
WORKER_ID = "worker-1"
TOTAL_CPU = 4
TOTAL_MEM = 8
HEARTBEAT_INTERVAL = 3  # seconds


def register_worker():
    url = f"{MASTER_BASE_URL}/api/workers/register"
    payload = {
        "worker_id": WORKER_ID,
        "host": socket.gethostbyname(socket.gethostname()),
        "total_cpu": TOTAL_CPU,
        "total_mem": TOTAL_MEM,
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        print("Register response:", response.status_code, response.text)
    except Exception as e:
        print("Failed to register worker:", repr(e))


def send_heartbeat():
    url = f"{MASTER_BASE_URL}/api/workers/heartbeat"
    payload = {
        "worker_id": WORKER_ID,
        "used_cpu": 0,
        "used_mem": 0,
        "running_tasks": [],
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        print("Heartbeat response:", response.status_code, response.text)
    except Exception as e:
        print("Failed to send heartbeat:", repr(e))


def main():
    print(f"Starting worker: {WORKER_ID}")
    register_worker()

    while True:
        send_heartbeat()
        time.sleep(HEARTBEAT_INTERVAL)


if __name__ == "__main__":
    main()