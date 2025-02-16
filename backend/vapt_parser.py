import pandas as pd

def parse_vapt_report(file):
    """Extracts vulnerability details from a VAPT report (XLS/CSV)"""
    df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
    vulnerabilities = []

    for _, row in df.iterrows():
        vulnerabilities.append({
            "name": row["Vulnerability Name"],
            "description": row["Description"],
            "impact": row["Impact"],
            "tech_stack": row["Tech Stack"],
            "vulnerable_url": row["Vulnerable URL"],
            "poc": row["Proof of Concept"]
        })

    return vulnerabilities