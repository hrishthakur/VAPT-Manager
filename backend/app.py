from flask import Flask, request, jsonify
from vapt_parser import parse_vapt_report
from ai_fix_generator import generate_fixes
from jira_integration import create_jira_ticket
from email_notifier import send_email
import database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def home():
    return "VAPT manager System API is running!", 200


@app.route("/upload-vapt", methods=["POST"])
def upload_vapt():
    """API Endpoint to upload and process VAPT report"""
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400

        # Validate file type
        if not file.filename.endswith((".xlsx", ".csv")):
            return jsonify(
                {
                    "status": "error",
                    "message": "Invalid file format. Only .xlsx and .csv files are supported",
                }
            ), 400

        vulnerabilities = parse_vapt_report(file)
        results = []

        for vuln in vulnerabilities:
            fixes = generate_fixes(vuln)
            if fixes:
                jira_response = create_jira_ticket(vuln, fixes)
                send_email(vuln, fixes)
                results.append(
                    {
                        "vulnerability": vuln["name"],
                        "jira_ticket": jira_response.get("key"),
                        "status": "processed",
                    }
                )
            else:
                logger.warning(
                    f"Could not generate fixes for vulnerability: {vuln['name']}"
                )
                results.append(
                    {
                        "vulnerability": vuln["name"],
                        "status": "failed",
                        "message": "Failed to generate fixes",
                    }
                )

        return jsonify(
            {
                "status": "success",
                "message": "VAPT report processed successfully",
                "results": results,
            }
        ), 200

    except Exception as e:
        logger.error(f"Error processing VAPT report: {str(e)}")
        return jsonify(
            {"status": "error", "message": f"Error processing VAPT report: {str(e)}"}
        ), 500


if __name__ == "__main__":
    app.run(debug=True)
