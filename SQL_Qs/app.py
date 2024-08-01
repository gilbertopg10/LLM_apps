import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Connection configuration mysql database
user = 'root'
password = os.getenv('mysql_pass')
host = 'localhost:3306'
database = 'Dhardware'

# DB object langchain
db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
db = SQLDatabase.from_uri(db_uri)

# template 1 
template_1 = """
           Based on the schema below, write a sql query that could answer the user's question.
              {schema}
              
              Question: {question}
              SQL Query:
              """
              
prompt_1 = ChatPromptTemplate.from_template(template_1)

# get schema function
def get_schema(_):
    return db.get_table_info()

# Model and query chain

# Initialize the groq model
llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=os.getenv('groq_api_key'))

# Define the SQL chain
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt_1
    | llm.bind(stop="\nSQL Result:")
    | StrOutputParser()
)

# template for final chain
template_2 = """  
Write a Response in natural language, based on the schema below, the sql query and the result of the query.

{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
"""

prompt_2 = ChatPromptTemplate.from_template(template_2)

# function to get the result of the query
def run_query(query):
    return db.run(query)

# final chain
full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response=lambda x: run_query(x['query']),
        )
    | prompt_2
    | llm
    | StrOutputParser()
)

# Streamlit app
st.title("Database Query App")

# Add a text input for the user's question
user_question = st.text_input("Enter your question about the database:")

# Add a button to submit the question
if st.button("Submit"):
    if user_question:
        # Process the question using your existing chain
        result = full_chain.invoke({"question": user_question})
        st.write("Answer:", result)
    else:
        st.warning("Please enter a question.")

