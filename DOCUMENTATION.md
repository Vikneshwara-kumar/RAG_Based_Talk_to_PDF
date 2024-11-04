# PDF QA Assistant Documentation

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details)
- [API Reference](#api-reference)
- [Configuration Options](#configuration-options)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The application follows a modular architecture with these main components:

1. **PDF Processing Pipeline**
   - PDF text extraction
   - Text chunking
   - Embedding generation
   - Vector store indexing

2. **Query Pipeline**
   - Context retrieval
   - Prompt construction
   - LLM response generation

3. **User Interface**
   - PDF upload and processing
   - Chat interface
   - Session management

## Component Details

### PDFQASystem Class

```python
class PDFQASystem:
    def __init__(self, groq_api_key: str):
        """
        Initialize the PDF QA System.
        Args:
            groq_api_key (str): The API key for Groq LLM service
        """

    def process_pdf(self, pdf_file) -> int:
        """
        Process a PDF file and create embeddings.
        Args:
            pdf_file: A file-like object containing the PDF
        Returns:
            int: Number of chunks processed
        """

    def generate_response(self, user_query: str, k: int = 4) -> str:
        """
        Generate a response using relevant context and Groq's LLM.
        Args:
            user_query (str): The user's question
            k (int): Number of relevant chunks to retrieve
        Returns:
            str: The generated response
        """
```

### Streamlit Interface

The interface is built using Streamlit and includes:
- Sidebar for configuration and PDF upload
- Main chat area for Q&A
- Session state management
- Error handling and user feedback

## API Reference

### Groq API

```python
chat_completion = groq_client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=1000,
)
```

### Vector Store (FAISS)

```python
vector_store = FAISS.from_texts(chunks, embeddings)
relevant_docs = vector_store.similarity_search(query, k=4)
```

## Configuration Options

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key

### Streamlit Secrets
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

### Model Parameters
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Temperature: 0.1
- Max tokens: 1000

## Development Guide

### Setting Up Development Environment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

```bash
pytest tests/
```

### Adding New Features

1. Create a new branch
2. Implement your feature
3. Add tests
4. Update documentation
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **PDF Processing Fails**
   - Check PDF file format
   - Ensure sufficient memory
   - Verify file permissions

2. **API Key Issues**
   - Verify API key is set
   - Check environment variables
   - Confirm Streamlit secrets

3. **Performance Issues**
   - Reduce chunk size
   - Adjust number of retrieved chunks
   - Optimize embedding model

### Debug Mode

Set `debug=True` in Streamlit config:
```toml
[server]
debug = true
```