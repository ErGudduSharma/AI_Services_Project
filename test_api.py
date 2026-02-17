import requests

url = "http://127.0.0.1:8000/run-workflow"
data = {"client_request": "Process a new loan application for a customer"}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", str(e))
