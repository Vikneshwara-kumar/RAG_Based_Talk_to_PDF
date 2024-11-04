import pytest
from src.utils import validate_api_key, create_prompt, clean_text, format_error_message

def test_validate_api_key_success():
    assert validate_api_key("gsk_valid1234567890abcdefghijklmnopqrstuv")

def test_validate_api_key_empty():
    with pytest.raises(ValueError, match="API key must be a non-empty string"):
        validate_api_key("")

def test_validate_api_key_invalid_format():
    with pytest.raises(ValueError, match="Invalid API key format"):
        validate_api_key("invalid_key")

def test_create_prompt():
    context = "Sample context"
    question = "Test question"
    prompt = create_prompt(context, question)
    
    assert context in prompt
    assert question in prompt
    assert "Context:" in prompt
    assert "Question:" in prompt
    assert "Answer:" in prompt

def test_clean_text():
    # Test removing extra whitespace
    assert clean_text("  extra  spaces  ") == "extra spaces"
    
    # Test removing special characters
    assert clean_text("Hello! @#$%^&* World?") == "Hello! World?"
    
    # Test keeping basic punctuation
    assert clean_text("Hello, world! How are you?") == "Hello, world! How are you?"
    
    # Test empty string
    assert clean_text("") == ""

def test_format_error_message():
    # Test with standard exception
    error = Exception("Test error")
    assert format_error_message(error) == "Error: Test error"
    
    # Test with nested exception
    try:
        raise ValueError("Nested error")
    except ValueError as e:
        assert format_error_message(e) == "Error: Nested error"