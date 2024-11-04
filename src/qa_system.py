from typing import List, Dict, Tuple
import groq
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from .pdf_processor import PDFProcessor
from .utils import create_prompt, validate_api_key

class PDFQASystem:
    """Main QA system for processing PDFs and generating responses using Groq LLM."""
    
    def __init__(self, groq_api_key: str):
        """
        Initialize the PDF QA System.
        
        Args:
            groq_api_key (str): API key for Groq's LLM service
        Raises:
            ValueError: If the API key is invalid
        """
        validate_api_key(groq_api_key)
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
        self.pdf_processor = PDFProcessor()

    def process_pdf(self, pdf_file) -> int:
        """
        Process a PDF file and create embeddings.
        
        Args:
            pdf_file: File object containing the PDF
        Returns:
            int: Number of chunks processed
        Raises:
            ValueError: If PDF processing fails
        """
        try:
            # Extract text from PDF
            pdf_text = self.pdf_processor.extract_text(pdf_file)
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(pdf_text)
            
            # Create vector store
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)
            
            return len(chunks)
        except Exception as e:
            raise ValueError(f"Failed to process PDF: {str(e)}")

    def generate_response(self, user_query: str, k: int = 4) -> str:
        """
        Generate a response using relevant context and Groq's LLM.
        
        Args:
            user_query (str): User's question
            k (int): Number of relevant chunks to retrieve
        Returns:
            str: Generated response
        Raises:
            ValueError: If no PDF has been processed or query fails
        """
        if not self.vector_store:
            raise ValueError("Please process a PDF document first.")

        try:
            # Retrieve relevant documents
            relevant_docs = self.vector_store.similarity_search(user_query, k=k)
            context = "\n".join(doc.page_content for doc in relevant_docs)

            # Create prompt
            prompt = create_prompt(context, user_query)

            # Generate response using Groq
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.1,
                max_tokens=1000,
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Failed to generate response: {str(e)}")

    def get_vector_store_stats(self) -> Dict[str, int]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dict[str, int]: Statistics including number of documents
        """
        if not self.vector_store:
            return {"num_documents": 0}
        return {
            "num_documents": len(self.vector_store.index_to_docstore_id)
        }