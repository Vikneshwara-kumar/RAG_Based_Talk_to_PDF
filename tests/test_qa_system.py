import pytest
from unittest.mock import Mock, patch
from src.qa_system import PDFQASystem

@pytest.fixture
def mock_groq_client():
    with patch('groq.Groq') as mock_groq:
        mock_instance = Mock()
        mock_groq.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def qa_system(mock_groq_client):
    return PDFQASystem("gsk_valid_api_key_for_testing")

def test_init_invalid_api_key():
    with pytest.raises(ValueError):
        PDFQASystem("")

def test_process_pdf_success(qa_system):
    # Mock PDF file and processing
    mock_pdf = Mock()
    mock_pdf.read.return_value = b"Sample PDF content"
    
    with patch('src.pdf_processor.PDFProcessor.extract_text') as mock_extract:
        mock_extract.return_value = "Sample text content"
        num_chunks = qa_system.process_pdf(mock_pdf)
        assert num_chunks > 0
        assert qa_system.vector_store is not None

def test_process_pdf_failure(qa_system):
    mock_pdf = Mock()
    mock_pdf.read.side_effect = Exception("PDF read error")
    
    with pytest.raises(ValueError):
        qa_system.process_pdf(mock_pdf)

def test_generate_response_no_pdf(qa_system):
    with pytest.raises(ValueError, match="Please process a PDF document first"):
        qa_system.generate_response("test query")

def test_generate_response_success(qa_system, mock_groq_client):
    # Setup mock vector store
    qa_system.vector_store = Mock()
    qa_system.vector_store.similarity_search.return_value = [
        Mock(page_content="relevant content")
    ]
    
    # Setup mock response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test response"))]
    mock_groq_client.chat.completions.create.return_value = mock_response
    
    response = qa_system.generate_response("test query")
    assert response == "Test response"

def test_get_vector_store_stats_empty(qa_system):
    stats = qa_system.get_vector_store_stats()
    assert stats["num_documents"] == 0

def test_get_vector_store_stats_with_documents(qa_system):
    # Mock vector store with documents
    qa_system.vector_store = Mock()
    qa_system.vector_store.index_to_docstore_id = {0: "doc1", 1: "doc2"}
    
    stats = qa_system.get_vector_store_stats()
    assert stats["num_documents"] == 2