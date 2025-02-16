import requests
import os

JIRA_API_URL = os.getenv("JIRA_API_URL")
JIRA_AUTH = (os.getenv("JIRA_USER"), os.getenv("JIRA_API_TOKEN"))

def create_jira_ticket(vulnerability, fixes):
    """Creates a JIRA ticket for the given vulnerability"""
    issue_data = {
        "fields": {
            "project": {"key": "SEC"},
            "summary": vulnerability["name"],
            "description": f"Issue: {vulnerability['description']}\nImpact: {vulnerability['impact']}\nFixes:\n{fixes}",
            "issuetype": {"name": "Bug"},
            "priority": {"name": "High"}
        }
    }

    response = requests.post(f"{JIRA_API_URL}/rest/api/2/issue", json=issue_data, auth=JIRA_AUTH)
    return response.json()
