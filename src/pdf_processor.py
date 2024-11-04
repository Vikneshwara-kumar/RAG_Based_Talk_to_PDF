from typing import List
from pypdf import PdfReader
import logging

class PDFProcessor:
    """Handles PDF file processing and text extraction."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.logger = logging.getLogger(__name__)

    def extract_text(self, pdf_file) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_file: File object containing the PDF
        Returns:
            str: Extracted text content
        Raises:
            ValueError: If text extraction fails
        """
        try:
            reader = PdfReader(pdf_file)
            text = ""
            
            # Extract text from each page
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            if not text.strip():
                raise ValueError("No text content extracted from PDF")
                
            return text
        except Exception as e:
            self.logger.error(f"Failed to extract text from PDF: {str(e)}")
            raise ValueError(f"PDF text extraction failed: {str(e)}")

    def get_metadata(self, pdf_file) -> dict:
        """
        Extract metadata from PDF file.
        
        Args:
            pdf_file: File object containing the PDF
        Returns:
            dict: PDF metadata
        """
        try:
            reader = PdfReader(pdf_file)
            return {
                "num_pages": len(reader.pages),
                "metadata": reader.metadata
            }
        except Exception as e:
            self.logger.error(f"Failed to extract metadata: {str(e)}")
            return {"num_pages": 0, "metadata": {}}