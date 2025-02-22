import pandas as pd
from typing import List, Dict
import logging


def parse_vapt_report(file) -> List[Dict]:
    """
    Extracts vulnerability details from a VAPT report (XLS/CSV)

    Args:
        file: File object containing the VAPT report

    Returns:
        List of dictionaries containing vulnerability details

    Raises:
        ValueError: If file format is not supported or required columns are missing
    """
    try:
        # Determine file type and read accordingly
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            raise ValueError(
                "Unsupported file format. Please upload .xlsx or .csv file"
            )

        # Verify required columns exist
        required_columns = [
            "Vulnerability Name",
            "Description",
            "Impact",
            "Tech Stack",
            "Vulnerable URL",
            "Proof of Concept",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        vulnerabilities = []
        for _, row in df.iterrows():
            # Clean and validate data
            vulnerability = {
                "name": str(row["Vulnerability Name"]).strip(),
                "description": str(row["Description"]).strip(),
                "impact": str(row["Impact"]).strip(),
                "tech_stack": str(row["Tech Stack"]).strip(),
                "vulnerable_url": str(row["Vulnerable URL"]).strip(),
                "poc": str(row["Proof of Concept"]).strip(),
            }

            # Only add if required fields are not empty
            if all(vulnerability.values()):
                vulnerabilities.append(vulnerability)
            else:
                logging.warning(f"Skipping row with missing values: {vulnerability}")

        return vulnerabilities

    except Exception as e:
        logging.error(f"Error parsing VAPT report: {str(e)}")
        raise
