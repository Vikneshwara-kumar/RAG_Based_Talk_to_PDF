# Project Structure

```
pdf-qa-assistant/
├── .gitignore              # Git ignore file
├── .streamlit/            # Streamlit configuration
│   └── secrets.toml       # API keys and secrets (not in git)
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── LICENSE               # Project license
├── README.md             # Project readme
├── DOCUMENTATION.md      # Detailed documentation
├── PROJECT_STRUCTURE.md  # This file
│
├── src/                  # Source code
│   ├── __init__.py
│   ├── pdf_processor.py  # PDF processing utilities
│   ├── qa_system.py     # Main QA system implementation
│   └── utils.py         # Helper functions
│
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_pdf_processor.py
│   ├── test_qa_system.py
│   └── test_utils.py
│
├── docs/                # Documentation files
│   ├── assets/         # Images and other assets
│   │   └── demo.gif    # Application demo
│   └── api/            # API documentation
│
└── examples/           # Example files and notebooks
    ├── sample.pdf      # Sample PDF for testing
    └── demo.ipynb      # Demo notebook
```

## Directory Details

### Root Directory Files
- `app.py`: Main Streamlit application entry point
- `requirements.txt`: Project dependencies
- Documentation files (README.md, DOCUMENTATION.md, etc.)

### Source Code (`src/`)
- `pdf_processor.py`: PDF processing and text extraction
- `qa_system.py`: Core QA system implementation
- `utils.py`: Helper functions and utilities

### Tests (`tests/`)
Contains test files corresponding to source code modules:
- Unit tests
- Integration tests
- Test fixtures and utilities

### Documentation (`docs/`)
- Technical documentation
- API references
- Assets (images, diagrams)
- User guides

### Examples (`examples/`)
- Sample files for testing
- Demonstration notebooks
- Usage examples

## Development Workflow

1. Source code changes go in `src/`
2. Add tests in `tests/`
3. Update documentation in `docs/`
4. Add examples in `examples/`

## Best Practices

1. Keep code modular and in appropriate directories
2. Maintain test coverage for new features
3. Update documentation when making changes
4. Use meaningful commit messages
5. Follow PEP 8 style guide

## Contributing

When adding new features:
1. Create feature branch from `main`
2. Add code in appropriate directory
3. Include tests and documentation
4. Submit pull request

## Version Control

```
.gitignore
├── .streamlit/secrets.toml
├── __pycache__/
├── *.pyc
├── venv/
└── .env
```

Important: Never commit sensitive information or large binary files.