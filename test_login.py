import json
import urllib.request
import urllib.error

print("=== Testing ChautariChic Login API ===")

# Test 1: Try admin login
print("\n1. Testing admin login...")
url = 'http://127.0.0.1:8000/api/accounts/login/'
data = {
    'email': 'admin@chautarichic.com',
    'password': 'Admin@123'
}

# Convert data to JSON
json_data = json.dumps(data).encode('utf-8')

try:
    # Create request
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    # Send request
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("✓ Login successful!")
        print("Status:", response.status)
        print("Response:", result)
        
except urllib.error.HTTPError as e:
    print("✗ HTTP Error:", e.code)
    error_body = e.read().decode('utf-8')
    print("Error details:", error_body)
except Exception as e:
    print("✗ Error:", e)

# Test 2: Check if API is accessible
print("\n2. Testing API endpoint...")
try:
    test_response = urllib.request.urlopen('http://127.0.0.1:8000/api/accounts/test/')
    test_data = json.loads(test_response.read().decode('utf-8'))
    print("✓ API is accessible")
    print("Test response:", test_data)
except Exception as e:
    print("✗ Cannot reach API:", e)
    print("Make sure server is running: python manage.py runserver")

print("\n=== Test Complete ===")