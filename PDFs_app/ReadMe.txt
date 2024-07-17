# Chat with Your Documents

This Streamlit application allows users to upload PDF documents and ask questions about their content using natural language processing and information retrieval.

## Features
- Multiple PDF document upload
- PDF text extraction
- Text processing and embedding creation
- Semantic search using FAISS
- Chat interface for asking questions about the documents
- Integration with OpenAI for AI-generated responses

## Requirements
- Python 3.7+
- Streamlit
- PyPDF2
- Langchain
- FAISS
- OpenAI API key

## Installation
1. Clone this repository:
2. Install the dependencies:
3. Create a `.env` file in the root directory and add your OpenAI API key:


## Usage
1. Run the application:
2. Open your browser and go to `http://localhost:8501`
3. Upload your PDF documents in the sidebar
4. Click "Process" to analyze the documents
5. Ask questions about the document content in the text input field

## Project Structure
- `app.py`: Main Streamlit application file
- `templates_html.py`: HTML templates for the user interface
- `style.css`: CSS styles for the application
- `requirements.txt`: List of project dependencies

## Contributing
Contributions are welcome. Please open an issue to discuss major changes before making a pull request.

