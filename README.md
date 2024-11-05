# RAG_Based_Talk_to_PDF

A Streamlit-based application that allows users to chat with their PDF documents using Groq's powerful LLM API. The application processes PDF documents, creates embeddings, and enables natural language querying of the document content.

![ RAG Based talk to PDF](https://raw.githubusercontent.com/Vikneshwara-kumar/RAG_Based_Talk_to_PDF/main/docs/assets/demo.gif)


## 🚀 Features

- 📄 PDF document processing and text extraction
- 🔍 Semantic search using FAISS vector store
- 💬 Interactive chat interface with document context
- 🤖 Powered by Groq's Mixtral-8x7b-32768 LLM
- 🔒 Secure API key management
- 💻 Easy-to-use Streamlit interface

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Vikneshwara-kumar/RAG_Based_Talk_to_PDF.git
cd RAG_Based_Talk_to_PDF
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Get your Groq API key from [Groq's website](https://console.groq.com)

2. Set up your API key in one of two ways:
   - Create `.streamlit/secrets.toml` file:
     ```toml
     GROQ_API_KEY = "your-groq-api-key-here"
     ```
   - Or set an environment variable:
     ```bash
     export GROQ_API_KEY='your-groq-api-key-here'
     ```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a PDF document and click "Process PDF"

4. Start asking questions about your document!

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://share.streamlit.io)
3. Create a new app and connect your forked repository
4. Add your `GROQ_API_KEY` to the Streamlit Cloud secrets
5. Deploy!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for their powerful LLM API
- [Streamlit](https://streamlit.io) for the amazing web framework
- [LangChain](https://langchain.org) for document processing utilities
- [FAISS](https://github.com/facebookresearch/faiss) for efficient similarity search
