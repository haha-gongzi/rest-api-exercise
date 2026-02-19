
# REST API In-class Exercise (FastAPI + openFDA)

This project implements a RESTful API using FastAPI. It supports user management,
text notes, and integration with the openFDA API.

---

## Environment Setup

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Run Server
uvicorn src.app:app --reload
Open in browser:

http://127.0.0.1:8000/docs

API Usage (PowerShell)
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
Add Note
$body = @{ text = "my first note" } | ConvertTo-Json
Invoke-RestMethod -Method Post `
 -Uri "http://127.0.0.1:8000/users/1/notes" `
 -ContentType "application/json" `
 -Body $body
List Notes
Invoke-RestMethod -Method Get `
 -Uri "http://127.0.0.1:8000/users/1/notes"
Final: Save openFDA Result as Note
$body = @{ query = "ibuprofen"; limit = 3; skip = 0 } | ConvertTo-Json
Invoke-RestMethod -Method Post `
 -Uri "http://127.0.0.1:8000/users/1/notes/from-fda" `
 -ContentType "application/json" `
 -Body $body
Tests
pytest
Author
Qinlin Zhang U78084337
Zhenyu Shi U47382655
Boston University

