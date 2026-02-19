# REST API In-class Exercise (FastAPI + openFDA)

This project implements a RESTful API using FastAPI. It supports user management,
text notes, and integration with the openFDA API.

---

## User Story

As a user, I want to search drug label information using the openFDA API and save
relevant drug information (brand name, generic name, purpose, and warnings) as a
personal note for later reference.

---

## Environment Setup

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Run Server
uvicorn src.app:app --reload
After starting the server, open:

http://127.0.0.1:8000/docs

to view the interactive API documentation.

Exercise 1: openFDA API Test (Python Requests)
The following script demonstrates how to query the openFDA API using Python
requests.

import requests

url = "https://api.fda.gov/drug/label.json"

params = {
    "search": "ibuprofen",
    "limit": 3,
    "skip": 0
}

response = requests.get(url, params=params, timeout=10)

print("Status Code:", response.status_code)

data = response.json()

if "results" in data:
    for item in data["results"]:
        brand = item.get("openfda", {}).get("brand_name", ["N/A"])[0]
        generic = item.get("openfda", {}).get("generic_name", ["N/A"])[0]
        print("Brand:", brand)
        print("Generic:", generic)
        print("-" * 20)
else:
    print("No results found.")
Exercise 2: REST API Usage (PowerShell)
Create User
$body = @{ username = "alice" } | ConvertTo-Json

Invoke-RestMethod -Method Post `
 -Uri "http://127.0.0.1:8000/users" `
 -ContentType "application/json" `
 -Body $body
Duplicate Username (409 Conflict)
try {
  $body = @{ username = "alice" } | ConvertTo-Json

  Invoke-RestMethod -Method Post `
   -Uri "http://127.0.0.1:8000/users" `
   -ContentType "application/json" `
   -Body $body
} catch {
  $_.Exception.Response.StatusCode.value__
}
Add Text Note
$body = @{ text = "my first note" } | ConvertTo-Json

Invoke-RestMethod -Method Post `
 -Uri "http://127.0.0.1:8000/users/1/notes" `
 -ContentType "application/json" `
 -Body $body
List User Notes
Invoke-RestMethod -Method Get `
 -Uri "http://127.0.0.1:8000/users/1/notes"
Final: Save openFDA Result as Note
This endpoint combines Exercise 1 and Exercise 2 by fetching drug label data from
openFDA and saving it as a user note.

$body = @{
  query = "ibuprofen"
  limit = 3
  skip = 0
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
 -Uri "http://127.0.0.1:8000/users/1/notes/from-fda" `
 -ContentType "application/json" `
 -Body $body
Tests
Basic API tests are implemented using pytest.

Run the tests with:

pytest
Project Structure
rest-api-exercise/
│
├── src/
│   ├── app.py
│   ├── models.py
│   ├── store.py
│   └── fda_client.py
│
├── tests/
│   └── test_api.py
│
├── README.md
└── requirements.txt
Author
Zhenyu Shi U47382655
Boston University

