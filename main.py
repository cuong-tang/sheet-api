from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Google Sheets setup
SHEET_ID = '1iuKe2NBzVteM1zBPdVRCetoeCV8vpyLXhVOtazHO9AY'
SHEET_NAME = 'Form Responses'  # Change if needed

# Authenticate using service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

@app.route("/rows", methods=["GET"])
def get_rows():
    data = sheet.get_all_records()
    return jsonify(data)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    data = sheet.get_all_records()
    results = [row for row in data if query in str(row).lower()]
    return jsonify(results)

app.run(host='0.0.0.0', port=8080)
