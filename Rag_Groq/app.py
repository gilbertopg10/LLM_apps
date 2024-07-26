import streamlit as st
import os
import shutil
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq

load_dotenv()

def read_pdf(file):
    text = ""
    for pdf in file:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text  

def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)
    return chunks

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=os.getenv("google_api_key"))

def delete_old_vectorstore():
    if os.path.exists("vectorstore"):
        shutil.rmtree("vectorstore")
        st.sidebar.info("Old vector store deleted.")

def create_vector_store(chunks):
    delete_old_vectorstore()  # Delete old vectorstore before creating a new one
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    vectorstore.save_local("vectorstore")
    return vectorstore

# define llm
llm = ChatGroq(api_key=os.getenv("groq_api_key"), model="llama-3.1-70b-versatile")

# define prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the following question based on the provided context.
Provide the most accurate and relevant information.

Context:
{context}

Question: {input}

Answer:
""")

def get_answer(user_input):
    # Create the document chain using the language model and prompt
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    # Initialize the retriever from the vector store
    retriever = st.session_state.vectorstore.as_retriever()

    # Create the retrieval chain by combining the retriever and document chain
    rag_chain = create_retrieval_chain(retriever, document_chain)

    # Invoke the retrieval chain with the user input and get the response
    response = rag_chain.invoke({"input": user_input})
    
    # Return the answer, not print it
    return response

def main():
    st.set_page_config(page_title="Document Processor", page_icon=":books:")

    with st.sidebar:
        st.subheader("Docs Portal")
        pdf_docs = st.file_uploader("Upload your docs here and click on 'Process':", type="pdf", 
                                    accept_multiple_files=True)
        
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing documents..."):
                    # read the pdf
                    text = read_pdf(pdf_docs)
                    # get the chunks
                    chunks = get_chunks(text)
                    # create a vector store
                    vectorstore = create_vector_store(chunks)
                    st.session_state.vectorstore = vectorstore
                    st.success("Docs processed and new vector store created!")
            else:
                st.warning("Please upload PDF documents first.")

    # Main area
    st.title("Document Processor")
    st.write("Use the sidebar to upload and process your documents.")

    if "vectorstore" in st.session_state:
        user_input = st.text_area("Enter your question:")
        if st.button("Get Answer"):
            if user_input:
                with st.spinner("Retrieving answer..."):
                    response = get_answer(user_input)
                    st.write(response['answer'])
                with st.expander("Show document similarity"):
                    # find the relevant chunks
                    for i, doc in enumerate(response['context']):
                        st.write(doc.page_content)
                        st.write("--------------------------")

if __name__ == "__main__":
    main()
