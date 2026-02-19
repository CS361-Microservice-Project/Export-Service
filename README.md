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
