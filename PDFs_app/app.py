import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from templates_html import user_template, bot_template

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def read_pdf(file):
    text = ""
    for pdf in file:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text    

def get_chunks(text):
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000,
                                     chunk_overlap=200, length_function=len)
    chunks = splitter.split_text(text)
    return chunks

def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store

def create_conversation_chain(vector_store):
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def main():
    st.set_page_config(page_title="Chat with your docs", page_icon=":books:")
    load_css('style.css')
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    st.header("Chat with your docs :books:")
    query = st.text_input("Ask questions about your docs:")
    
    if query:
        if st.session_state.conversation is None:
            st.warning("Please upload and process documents before asking questions.")
        else:
            response = st.session_state.conversation({"question": query})
            st.session_state.chat_history.append(("user", query))
            st.session_state.chat_history.append(("bot", response['answer']))

    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(user_template.replace("{user_message}", message), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{bot_message}", message), unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Your docs")
        pdf_docs = st.file_uploader("Upload your docs here and click on 'Process':", type="pdf", 
                                    accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing..."):
                
                # get the pdf text
                if pdf_docs:
                    raw_text = read_pdf(pdf_docs)
                else:
                    st.error("Please upload at least one PDF document.")
                    return
                    
                # get the chunks of text
                chunks = get_chunks(raw_text)
                
                # create the vector store
                vecstore = create_vector_store(chunks)
                
                # Create the chain of conversation
                st.session_state.conversation = create_conversation_chain(vecstore)
                
                st.success("Processing complete!")

if __name__ == "__main__":
    main()