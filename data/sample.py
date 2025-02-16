import pandas as pd

# Define sample VAPT data
data = {
    "Vulnerability Name": ["SQL Injection", "XSS", "Insecure Deserialization"],
    "CWE ID": ["CWE-89", "CWE-79", "CWE-502"],
    "Description": [
        "User input is directly injected into SQL query.",
        "Unsanitized user input in web page output.",
        "Deserializing untrusted data leads to remote code execution."
    ],
    "Impact": ["High", "Medium", "Critical"],
    "Common Recommendations": [
        "Use ORM or Parameterized Queries.",
        "Use output encoding or CSP.",
        "Use digital signatures or validation."
    ],
    "Tech Stack": ["Python + Django", "JavaScript + React", "Java + Spring Boot"],
    "Vulnerable URL": ["/login", "/search?q=", "/api/upload"],
    "POC": ["' OR 1=1 --", "<script>alert('XSS')</script>", "Malicious serialized object"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save as an Excel file
df.to_excel("sample_vapt_report.xlsx", index=False)

print("Sample VAPT report 'sample_vapt_report.xlsx' generated successfully.")
