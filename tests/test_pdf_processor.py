import pytest
from unittest.mock import Mock, patch
from src.pdf_processor import PDFProcessor

@pytest.fixture
def pdf_processor():
    return PDFProcessor()

def test_extract_text_success(pdf_processor):
    # Mock PDF file with content
    mock_pdf = Mock()
    
    with patch('pypdf.PdfReader') as mock_reader:
        # Setup mock pages
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 content"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 content"
        
        mock_reader.return_value.pages = [mock_page1, mock_page2]
        
        text = pdf_processor.extract_text(mock_pdf)
        assert "Page 1 content" in text
        assert "Page 2 content" in text

def test_extract_text_empty_pdf(pdf_processor):
    mock_pdf = Mock()
    
    with patch('pypdf.PdfReader') as mock_reader:
        mock_page = Mock()
        mock_page.extract_text.return_value = ""
        mock_reader.return_value.pages = [mock_page]
        
        with pytest.raises(ValueError, match="No text content extracted from PDF"):
            pdf_processor.extract_text(mock_pdf)

def test_extract_text_pdf_error(pdf_processor):
    mock_pdf = Mock()
    
    with patch('pypdf.PdfReader') as mock_reader:
        mock_reader.side_effect = Exception("PDF read error")
        
        with pytest.raises(ValueError, match="PDF text extraction failed"):
            pdf_processor.extract_text(mock_pdf)

def test_get_metadata_success(pdf_processor):
    mock_pdf = Mock()
    
    with patch('pypdf.PdfReader') as mock_reader:
        mock_reader.return_value.pages = [Mock(), Mock()]  # 2 pages
        mock_reader.return_value.metadata = {"Author": "Test Author"}
        
        metadata = pdf_processor.get_metadata(mock_pdf)
        assert metadata["num_pages"] == 2
        assert metadata["metadata"]["Author"] == "Test Author"

def test_get_metadata_error(pdf_processor):
    mock_pdf = Mock()
    
    with patch('pypdf.PdfReader') as mock_reader:
        mock_reader.side_effect = Exception("Metadata read error")
        
        metadata = pdf_processor.get_metadata(mock_pdf)
        assert metadata["num_pages"] == 0
        assert metadata["metadata"] == {}