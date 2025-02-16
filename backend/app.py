from flask import Flask, request, jsonify
from vapt_parser import parse_vapt_report
from ai_fix_generator import generate_fixes
from jira_integration import create_jira_ticket
from email_notifier import send_email
import database

app = Flask(__name__)

@app.route('/')
def home():
    return "VAPT manager System API is running!", 200

@app.route('/upload-vapt', methods=['POST'])
def upload_vapt():
    """API Endpoint to upload and process VAPT report"""
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    vulnerabilities = parse_vapt_report(file)
    for vuln in vulnerabilities:
        fixes = generate_fixes(vuln)
        create_jira_ticket(vuln, fixes)
        send_email(vuln, fixes)

    return jsonify({"message": "VAPT report processed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)