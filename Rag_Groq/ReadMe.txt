# Document Processor

## Description
This Streamlit application allows users to upload PDF documents, process them, and ask questions about their content. It uses natural language processing and machine learning techniques to provide accurate answers based on the uploaded documents.

## Features
- PDF document upload and processing
- Question-answering system based on document content
- Document similarity display
- Vector store management for efficient retrieval

## Technologies Used
- Streamlit: For the web application interface
- PyPDF2: For reading PDF files
- LangChain: For text processing and retrieval
- FAISS: For efficient similarity search and clustering of dense vectors
- Google Generative AI: For text embeddings
- Groq: For the language model

## Requirements
The application requires the following packages:
faiss-cpu
groq
langchain-groq
PyPDF2
langchain
streamlit
langchain_community
python-dotenv
pypdf
langchain_google_genai
Copy
## Setup and Installation
1. Clone the repository
2. Install the required packages:
pip install -r requirements.txt
Copy3. Set up environment variables:
- Create a `.env` file in the project root
- Add the following variables:
  ```
  google_api_key=your_google_api_key
  groq_api_key=your_groq_api_key
  ```

## Usage
1. Run the Streamlit app:
streamlit run app.py
Copy2. Use the sidebar to upload PDF documents
3. Click "Process" to analyze the documents
4. Enter questions in the main area and click "Get Answer"
5. View answers and related document sections

## Functions
- `read_pdf(file)`: Extracts text from uploaded PDF files
- `get_chunks(text)`: Splits text into manageable chunks
- `delete_old_vectorstore()`: Removes previous vector store data
- `create_vector_store(chunks)`: Creates a new vector store from text chunks
- `get_answer(user_input)`: Retrieves answers based on user questions
- `main()`: Main function to run the Streamlit application

## Notes
- The application uses Google's Generative AI for embeddings and Groq's LLM for question answering
- A new vector store is created each time documents are processed, replacing the old one
- Document similarity can be viewed for each answer



