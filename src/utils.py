import re
from typing import Optional

def validate_api_key(api_key: str) -> bool:
    """
    Validate Groq API key format.
    
    Args:
        api_key (str): API key to validate
    Returns:
        bool: True if valid
    Raises:
        ValueError: If API key is invalid
    """
    if not api_key or not isinstance(api_key, str):
        raise ValueError("API key must be a non-empty string")
    
    # Basic format validation - modify based on actual Groq API key format
    if not re.match(r'^gsk_[a-zA-Z0-9]{32,}$', api_key):
        raise ValueError("Invalid API key format")
    
    return True

def create_prompt(context: str, question: str) -> str:
    """
    Create a prompt for the LLM using context and question.
    
    Args:
        context (str): Retrieved document context
        question (str): User's question
    Returns:
        str: Formatted prompt
    """
    return f"""Using the following context, please answer the user's question. 
    If the answer cannot be found in the context, say so.

    Context:
    {context}

    Question: {question}

    Answer:"""

def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text (str): Text to clean
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()

def format_error_message(error: Exception) -> str:
    """
    Format error message for user display.
    
    Args:
        error (Exception): Error to format
    Returns:
        str: Formatted error message
    """
    return f"Error: {str(error)}"