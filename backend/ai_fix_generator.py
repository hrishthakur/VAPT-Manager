import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_fixes(vulnerability):
    """Uses GPT-4 to generate security fixes based on extracted vulnerability details"""
    prompt = f"""
    Vulnerability: {vulnerability["name"]}
    Description: {vulnerability["description"]}
    Impact: {vulnerability["impact"]}
    Tech Stack: {vulnerability["tech_stack"]}

    Provide three security fixes:
    1. Best Security Fix (Fully Secure)
    2. Business-Friendly Fix (Minimal Downtime)
    3. Temporary Mitigation (Quick Patch)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]
