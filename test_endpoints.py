import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("=== Testing Finance Dashboard API ===")
    
    # 1. Create Admin User
    print("\n1. Creating Admin User...")
    admin_data = {
        "email": "admin@example.com",
        "password": "adminpassword",
        "full_name": "Admin User",
        "role": "Admin"
    }
    resp = requests.post(f"{BASE_URL}/users/", json=admin_data)
    if resp.status_code in [200, 201]:
        print("SUCCESS: Admin user created.")
    elif resp.status_code == 400:
        print("INFO: Admin user already exists.")
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")

    # 2. Login as Admin
    print("\n2. Logging in as Admin...")
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword"
    }
    resp = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
    if resp.status_code == 200:
        admin_token = resp.json()["access_token"]
        print("SUCCESS: Logged in as Admin.")
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")
        return
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Create a Transaction as Admin
    print("\n3. Creating Transaction as Admin...")
    tx_data = {
        "amount": 5000.0,
        "type": "Income",
        "category": "Salary",
        "notes": "Monthly salary"
    }
    resp = requests.post(f"{BASE_URL}/transactions/", json=tx_data, headers=admin_headers)
    if resp.status_code == 200:
        print("SUCCESS: Transaction created.")
        tx_id = resp.json()["id"]
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")

    # 4. Get Dashboard Summary
    print("\n4. Getting Dashboard Summary...")
    resp = requests.get(f"{BASE_URL}/dashboard/summary", headers=admin_headers)
    if resp.status_code == 200:
        summary = resp.json()
        print(f"SUCCESS: Dashboard summary retrieved. Total Income: {summary['total_income']}")
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")

    # 5. Create Analyst User
    print("\n5. Creating Analyst User...")
    analyst_data = {
        "email": "analyst@example.com",
        "password": "analystpassword",
        "full_name": "Analyst User",
        "role": "Analyst"
    }
    resp = requests.post(f"{BASE_URL}/users/", json=analyst_data)
    if resp.status_code in [200, 201]:
        print("SUCCESS: Analyst user created.")
    elif resp.status_code == 400:
        print("INFO: Analyst user already exists.")
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")

    # 6. Login as Analyst
    print("\n6. Logging in as Analyst...")
    login_data = {
        "username": "analyst@example.com",
        "password": "analystpassword"
    }
    resp = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
    if resp.status_code == 200:
        analyst_token = resp.json()["access_token"]
        print("SUCCESS: Logged in as Analyst.")
    else:
        print(f"FAILED: Status {resp.status_code}, {resp.text}")
        return
    
    analyst_headers = {"Authorization": f"Bearer {analyst_token}"}

    # 7. Analyst attempt to create transaction (should fail)
    print("\n7. Analyst attempting to create transaction (RBAC Test)...")
    tx_data = {
        "amount": 200.0,
        "type": "Expense",
        "category": "Food",
        "notes": "Lunch"
    }
    resp = requests.post(f"{BASE_URL}/transactions/", json=tx_data, headers=analyst_headers)
    if resp.status_code == 403:
        print("SUCCESS: RBAC working. Analyst forbidden from creating transactions.")
    else:
        print(f"UNEXPECTED: Analyst got status {resp.status_code}")

    # 8. Analyst view dashboard (should work)
    print("\n8. Analyst viewing dashboard...")
    resp = requests.get(f"{BASE_URL}/dashboard/summary", headers=analyst_headers)
    if resp.status_code == 200:
        print("SUCCESS: Analyst can see dashboard.")
    else:
        print(f"FAILED: Analyst status {resp.status_code}")

    print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    test_api()
