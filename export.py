# Export Microservice - A small REST service that exports a list of records to a CSV file.
# Uses Flask + Python's built-in csv module.

from flask import Flask, request, jsonify
import csv
import os


# app: The Flask web server object.
app = Flask(__name__)


# EXPORT_DIR: Folder where CSV files are saved.
# This creates a simple local folder named "exports" next to this script.
EXPORT_DIR = "exports"


# is_valid_record_list: Checks that data is a list of dictionaries (records).
# Prerequisites: None.
# Arguments: data (any).
# Returns: bool, True if valid list of dict records; False otherwise.
def is_valid_record_list(data):
    # Data must be a list.
    if type(data) is not list:
        return False

    # Each item must be a dictionary.
    for item in data:
        if type(item) is not dict:
            return False

    return True


# get_fieldnames: Builds the CSV column list from the record keys.
# Prerequisites: records is a list of dicts (can be empty).
# Arguments: records (list of dict).
# Returns: list of str fieldnames.
def get_fieldnames(records):
    # No records means no columns.
    if len(records) == 0:
        return []

    # Start with the first record's keys so column order is predictable.
    fieldnames = []
    for key in records[0].keys():
        fieldnames.append(str(key))

    # Add any keys that show up in later records.
    for rec in records[1:]:
        for key in rec.keys():
            key_str = str(key)
            if key_str not in fieldnames:
                fieldnames.append(key_str)

    return fieldnames


# safe_filename: Cleans up a filename and makes sure it ends in .csv.
# Prerequisites: name is a string or None.
# Arguments: name (str or None).
# Returns: str, safe filename ending in .csv.
def safe_filename(name):
    # If no name is provided, use a default.
    if type(name) is not str or name.strip() == "":
        return "export.csv"

    # Keep only simple filename characters.
    cleaned = ""
    for ch in name.strip():
        if ch.isalnum() or ch in "-_.":
            cleaned += ch

    # If it got cleaned down to nothing, fall back to default.
    if cleaned == "":
        cleaned = "export.csv"

    # Make sure it ends with .csv
    if not cleaned.lower().endswith(".csv"):
        cleaned += ".csv"

    return cleaned


# write_csv_file: Writes the records to a CSV file on disk.
# Prerequisites: records is a non-empty list of dicts.
# Arguments: records (list of dict), filepath (str).
# Returns: None.
def write_csv_file(records, filepath):
    # Determine CSV columns from the record keys.
    fieldnames = get_fieldnames(records)

    # newline="" prevents blank lines on Windows.
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")

        # Write header row.
        writer.writeheader()

        # Write each record as a row.
        for rec in records:
            # Convert values to strings so the CSV is consistent.
            row = {}
            for k in fieldnames:
                val = rec.get(k, "")
                row[k] = "" if val is None else str(val)
            writer.writerow(row)


# export_data: Endpoint for POST /export.
# Prerequisites: Request must be JSON with key "data" containing a list of record dicts.
# Optional: "filename" lets the client pick the output file name.
# Arguments: None (uses Flask request).
# Returns: JSON response:
#   Success: {"status": "ok", "filename": "<name>", "path": "exports/<name>"}
#   No data: {"status": "error", "error_message": "There is no data to export."}
#   Bad input: {"status": "error", "error_message": "Invalid request format."}
@app.post("/export")
def export_data():
    # Read JSON body. silent=True returns None instead of throwing an error.
    body = request.get_json(silent=True)

    # Body must be a JSON object.
    if type(body) is not dict:
        return jsonify({"status": "error", "error_message": "Invalid request format."}), 400

    # Pull the data list from the JSON.
    data = body.get("data")

    # Validate data type (must be list of dict records).
    if not is_valid_record_list(data):
        return jsonify({"status": "error", "error_message": "Invalid request format."}), 400

    # Empty list means nothing to export.
    if len(data) == 0:
        return jsonify({"status": "error", "error_message": "There is no data to export."}), 200

    # Make sure the exports folder exists.
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # Choose a safe filename.
    filename = safe_filename(body.get("filename"))

    # Write the CSV file.
    filepath = os.path.join(EXPORT_DIR, filename)
    write_csv_file(data, filepath)

    # Return success info.
    return jsonify({"status": "ok", "filename": filename, "path": filepath}), 200


# main: Starts the Flask server on localhost port 5002.
# Prerequisites: Flask installed.
# Arguments: None.
# Returns: None (runs until stopped).
def main():
    app.run(host="127.0.0.1", port=5002, debug=False)


main()