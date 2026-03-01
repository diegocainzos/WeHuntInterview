import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_webhook_hardware():
    print("--- Sending Hardware Alert ---")
    payload = {
        "alert_id": "ZB-999",
        "server_id": "production-web-01",
        "data": "SSD S.M.A.R.T. Failure Prediction on /dev/sda",
        "urgency_level": 4
    }
    response = requests.post(f"{BASE_URL}/webhook", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_webhook_network():
    print("--- Sending Network Alert ---")
    payload = {
        "alert_id": "ZB-888",
        "server_id": "core-db-02",
        "data": "BGP Session Down: Neighbor Peer 10.0.0.1",
        "urgency_level": 5
    }
    response = requests.post(f"{BASE_URL}/webhook", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Note: Ensure the FastAPI server is running with:
    # uvicorn playground:app --reload
    try:
        test_webhook_hardware()
        test_webhook_network()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to FastAPI server. Is it running?")
