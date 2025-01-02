import streamlit as st
import os
from typing import List, Dict
import groq
from pypdf import PdfReader
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import textwrap
import tempfile

class PDFQASystem:
    def __init__(self, groq_api_key: str):
        """Initialize the PDF QA System with necessary components."""
        self.groq_client = groq.Groq(api_key=groq_api_key)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None

    def process_pdf(self, pdf_file) -> None:
        """Process a PDF file and create embeddings."""
        pdf_text = self._extract_text_from_pdf(pdf_file)
        chunks = self.text_splitter.split_text(pdf_text)
        self.vector_store = FAISS.from_texts(chunks, self.embeddings)
        return len(chunks)

    def _extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text content from a PDF file."""
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
         
    def generate_response(self, user_query: str, k: int = 4) -> str:
        """Generate a response using relevant context and Groq's LLM."""
        if not self.vector_store:
            return "Please upload a PDF document first."

        relevant_docs = self.vector_store.similarity_search(user_query, k=k)
        context = "\n".join(doc.page_content for doc in relevant_docs)




        prompt = f"""You are a helpful assistant. Using the following context, please answer the user's question as detailed as possible from the provided context, make sure to provide all the details. 
        If the answer cannot be found in the context, say so.

        Context:
        {context}

        Question: {user_query}

        Please structure your response as follows:
        - **Key Points**: List each main point in bullet points.
        - **Summary**: Provide a brief paragraph summarizing the main findings.

        Answer:"""

        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=2048,
        )

        return chat_completion.choices[0].message.content

def initialize_session_state():
    """Initialize session state variables."""
    if 'qa_system' not in st.session_state:
        groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if groq_api_key:
            st.session_state.qa_system = PDFQASystem(groq_api_key)
        else:
            st.session_state.qa_system = None
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    st.set_page_config(page_title="RAG Based talk to PDF", layout="wide")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("📚 RAG Based talk to PDF")
        
        # API Key input
        if not st.secrets.get("GROQ_API_KEY") and not os.getenv("GROQ_API_KEY"):
            groq_api_key = st.text_input("Enter your Groq API Key:", type="password")
            if groq_api_key:
                st.session_state.qa_system = PDFQASystem(groq_api_key)
        
        # PDF upload
        uploaded_file = st.file_uploader("Upload your PDF", type=['pdf'])
        
        if uploaded_file and st.session_state.qa_system:
            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    num_chunks = st.session_state.qa_system.process_pdf(uploaded_file)
                    st.session_state.pdf_processed = True
                    st.success(f"✅ PDF processed into {num_chunks} chunks!")
        
        # Display chat history length
        if st.session_state.chat_history:
            st.info(f"💬 Chat history: {len(st.session_state.chat_history)} messages")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Main chat interface
    st.title("Chat with your PDF 💬")
    
    # Check if system is ready
    if not st.session_state.qa_system:
        st.error("⚠️ Please enter your Groq API key in the sidebar to begin.")
        return
    
    if not st.session_state.pdf_processed:
        st.warning("⚠️ Please upload and process a PDF file to begin chatting.")
        return
    
    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.qa_system.generate_response(prompt)
                st.write(response)
        
        # Update chat history
        st.session_state.chat_history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ])

if __name__ == "__main__":
    main()