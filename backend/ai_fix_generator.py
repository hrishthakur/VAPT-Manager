import openai
import os
from typing import Dict, Optional
from logging import getLogger

# Set up logging
logger = getLogger(__name__)

# Validate API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_fixes(vulnerability: Dict[str, str]) -> Optional[str]:
    """
    Uses GPT-3.5-turbo to generate security fixes based on extracted vulnerability details.
    
    Args:
        vulnerability: Dictionary containing vulnerability details including name,
                      description, impact and tech stack.
    
    Returns:
        Generated security fixes as a string, or None if API call fails.
        
    Raises:
        openai.error.OpenAIError: If there is an error calling the OpenAI API
    """
    prompt = f"""
    Based on the following vulnerability details, provide three detailed security fixes with implementation steps:
    
    VULNERABILITY DETAILS
    --------------------
    Name: {vulnerability["name"]}
    Description: {vulnerability["description"]} 
    Impact: {vulnerability["impact"]}
    Technology Stack: {vulnerability["tech_stack"]}

    Please provide three comprehensive security fixes:

    1. BEST PRACTICE FIX
    - Full security solution
    - Implementation steps
    - Required resources
    - Expected timeline
    
    2. BUSINESS-OPTIMIZED FIX  
    - Balanced security/business solution
    - Implementation with minimal disruption
    - Resource requirements
    - Estimated downtime
    
    3. TEMPORARY MITIGATION
    - Quick temporary fix
    - Implementation steps
    - Limitations
    - Follow-up requirements
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Using free model instead of GPT-4
            messages=[
                {"role": "system", "content": "You are a senior security engineer providing detailed vulnerability remediation advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response["choices"][0]["message"]["content"]
        
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return None
