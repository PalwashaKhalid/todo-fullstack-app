"""
Manual API test script to verify Task endpoints.
Run this to test the API without pytest.
"""
import requests
from jose import jwt
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8001"
JWT_SECRET = "UQ29TeyfymBzSA2hHEIyiZ/jqJAcikfM3xhqIJH1ZMY="

# Generate a test JWT token
def create_test_token(user_id=1, email="test@example.com"):
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def test_health_check():
    print("\n1. Testing health check endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_create_task(token):
    print("\n2. Testing task creation...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": "Test Task", "description": "Test Description"}
    response = requests.post(f"{BASE_URL}/api/tasks/", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 201
    return response.json()["id"]

def test_list_tasks(token):
    print("\n3. Testing task listing...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_get_task(token, task_id):
    print(f"\n4. Testing get task by ID ({task_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_update_task(token, task_id):
    print(f"\n5. Testing task update ({task_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": "Updated Task", "description": "Updated Description"}
    response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_update_task_status(token, task_id):
    print(f"\n6. Testing task status update ({task_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"completed": True}
    response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}/status", json=data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_delete_task(token, task_id):
    print(f"\n7. Testing task deletion ({task_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    print(f"   Status: {response.status_code}")
    assert response.status_code == 204

def test_unauthorized_access():
    print("\n8. Testing unauthorized access (no token)...")
    data = {"title": "Unauthorized Task"}
    response = requests.post(f"{BASE_URL}/api/tasks/", json=data)
    print(f"   Status: {response.status_code}")
    assert response.status_code == 403

if __name__ == "__main__":
    print("=" * 60)
    print("Backend API Manual Test Suite")
    print("=" * 60)
    
    try:
        # Generate test token
        token = create_test_token()
        print(f"\nGenerated test JWT token for user_id=1")
        
        # Run tests
        test_health_check()
        task_id = test_create_task(token)
        test_list_tasks(token)
        test_get_task(token, task_id)
        test_update_task(token, task_id)
        test_update_task_status(token, task_id)
        test_delete_task(token, task_id)
        test_unauthorized_access()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
