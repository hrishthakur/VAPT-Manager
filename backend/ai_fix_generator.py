import openai
from openai import OpenAI
import os
from typing import Dict, Optional
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_openai_api_key() -> None:
    """Initialize OpenAI client with API key from environment variables."""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )

        # Initialize OpenAI client without proxies
        global client
        client = OpenAI(api_key=api_key)

        # Configure legacy openai module
        openai.api_key = api_key
        openai.proxy = None  # Explicitly disable proxy

        logger.info("OpenAI API key configured successfully")

    except Exception as e:
        logger.error(f"Error setting OpenAI API key: {str(e)}")
        raise


try:
    set_openai_api_key()
except Exception as e:
    logger.error(
        f"Failed to initialize OpenAI API. Application may not function correctly. Error: {str(e)}"
    )


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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior security engineer providing detailed vulnerability remediation advice.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content

    except openai.AuthenticationError as e:
        logger.error(f"Authentication error: {str(e)}")
    except openai.RateLimitError as e:
        logger.error(f"Rate limit error: {str(e)}")
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
    return None
