import pytest
import requests
from mock_data import SAMPLE_BIDDING_WEBHOOK, SAMPLE_PENDING_WEBHOOK

def test_webhook_bidding():
    """Test webhook with BIDDING state"""
    response = requests.post(
        "http://flask-app:8080/webhook",
        json=SAMPLE_BIDDING_WEBHOOK,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["created", "test_success"]
    print(f"\nBIDDING webhook response: {data}")

def test_webhook_pending():
    """Test webhook with PENDING state"""
    response = requests.post(
        "http://flask-app:8080/webhook",
        json=SAMPLE_PENDING_WEBHOOK,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    print(f"\nPENDING webhook response: {data}")

if __name__ == "__main__":
    print("\nTesting BIDDING state webhook:")
    test_webhook_bidding()
    
    print("\nTesting PENDING state webhook:")
    test_webhook_pending()