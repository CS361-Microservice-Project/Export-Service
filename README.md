# Export Microservice (Flask)
A simple REST microservice that exports records to a CSV file.

## What it does
- Accepts a list of records via `POST /export`
- Uses record keys as CSV headers
- Writes a `.csv` file into a local `exports/` folder
- Returns the saved filename/path in a JSON response

## Requirements
- Python 3.x
- Flask

## How to Request Data

To request data export, send a `POST` request to the `/export` endpoint with a JSON array of records in the request body.

### Endpoint
```
POST /export
```

### Headers
```
Content-Type: application/json
```

### Request Body Format

The request body must be a JSON array.  
Each object in the array represents one row that will be written to the CSV file.

### Example Request Body
```json
[
  { "id": 1, "name": "Erwin", "email": "erwin@example.com" },
  { "id": 2, "name": "Peter", "email": "peter@example.com" }
]
```

## Requesting Data from the Microservice (Example Call)

Below is an example of how a client program can send a request to the Export Microservice using Python.

```python
import requests

url = "http://localhost:5000/export"

data = [
  { "id": 1, "name": "Erwin", "email": "erwin@example.com" },
  { "id": 2, "name": "Peter", "email": "peter@example.com" }
]

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
```

## How to Receive Data 

After sending a `POST` request to `/export`, the microservice processes the provided JSON data and returns a JSON response.

### Success Response

If the export is successful, the microservice returns:

```json
{
  "status": "ok",
  "filename": "export_2026-02-23_123456.csv",
  "path": "exports/export_2026-02-23_123456.csv"
}
```

- `status` indicates whether the request was successful.
- `filename` is the generated CSV file name.
- `path` is the location of the saved file inside the `exports/` directory.

### Error Responses

If there is no data to export:

```json
{
  "status": "error",
  "error_message": "There is no data to export."
}
```

If the request format is invalid:

```json
{
  "status": "error",
  "error_message": "Invalid request format."
}
```

---

## Example Call (Receiving Data in the Client)

Below is an example of how a client program can handle the JSON response returned by the microservice.

```python
result = response.json()

if result["status"] == "ok":
    print("Export successful.")
    print("File saved at:", result["path"])
else:
    print("Export failed:", result["error_message"])
```
