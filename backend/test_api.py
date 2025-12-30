import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_create_request():
    """Test POST /api/requests"""
    print("\n=== Testing POST /api/requests ===")
    payload = {
        "title": "Add Login System",
        "description": "Need to add OAuth login for admin panel",
        "request_type": "NEW_REQUEST",
        "business_unit": "IT",
        "priority": "HIGH",
        "submitted_by": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/requests/", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, default=str)}")
        return result.get("id")
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_list_requests():
    """Test GET /api/requests"""
    print("\n=== Testing GET /api/requests ===")
    try:
        response = requests.get(f"{BASE_URL}/api/requests/")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {len(result)} requests")
        print(json.dumps(result, indent=2, default=str))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_get_request_details(request_id):
    """Test GET /api/requests/{id}"""
    print(f"\n=== Testing GET /api/requests/{request_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/api/requests/{request_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing MAIR API Endpoints")
    
    # Test create
    request_id = test_create_request()
    
    # Test list
    requests_list = test_list_requests()
    
    # Test get details if we got an ID
    if request_id:
        test_get_request_details(request_id)
    elif requests_list:
        test_get_request_details(requests_list[0]["id"])
    
    print("\n✅ Testing complete!")
