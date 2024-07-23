from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import datetime
import streamlit as st
import shutil
from llama_index.llms.groq import Groq
from math import ceil
from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
from llama_index.core.program import LLMTextCompletionProgram, FunctionCallingProgram
from llama_index.core.output_parsers import PydanticOutputParser
import json
import math
import pandas as pd



load_dotenv()

def scrap_data(url):
    load_dotenv()
    # Initialize the FirecrawlApp object
    app = FirecrawlApp(api_key=os.getenv('fire_crawl_apikey'))
    
    #Scrap a single URL
    result = app.scrape_url(url)
    
    # Check if markdown key data exists
    if 'markdown' in result:
        # Return the markdown data
        return result['markdown']
    else:
        # raise key error
        raise KeyError('Markdown key not found in the result')

def save_raw_data(data, timestamp, output_folder='raw_data'):
    # check if the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # save the raw markdown data with timestamp in filename
    raw_output_file = os.path.join(output_folder, f'raw_data_{timestamp}.md')
    with open(raw_output_file, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f'Raw data saved to {raw_output_file}')

def delete_files_in_directory(directory):
    try:
        # Remove all files and subdirectories
        shutil.rmtree(directory)
        # Recreate the empty directory
        os.makedirs(directory, exist_ok=True)
        print(f"All files in {directory} have been deleted.")
    except Exception as e:
        print(f"Error deleting files in {directory}: {e}")

# initialize the llm from groq model

llama3 = Groq(model = "llama-3.1-70b-versatile", api_key=os.getenv('groq_apikey'),temperature=0.0)   

# Define the classes

# Define the classes

class RealEstateProperty(BaseModel):
    address: Optional[str] = Field(description="The address of the property")
    price: Optional[str] = Field(description="The price of the property")
    property_type: Optional[str] = Field(description="The type of the property")
    bedrooms: Optional[str] = Field(description="The number of bedrooms")
    bathrooms: Optional[str] = Field(description="The number of bathrooms")
    square_footage: Optional[str] = Field(description="The square footage of the property")

class Listing(BaseModel):
    properties: List[RealEstateProperty] = Field(description="List of real estate properties")
    
    
# Initialize the extractor

prompt_template_str = """/
you are an intelligent text extraction and conversion assistant.

if you do not have the information about a certain field, please leave it empty.

get from each property the following information:
- address
- price
- property type
- bedrooms
- bathrooms
- square footage


{document}
"""

pydantic_data_extractor = LLMTextCompletionProgram.from_defaults(
    output_parser=PydanticOutputParser(Listing),
    prompt_template_str=prompt_template_str,
    llm=llama3
)





def save_chunks(document, chunk_size=15000, output_folder='chunks'):
    # Calculate the number of chunks
    num_chunks = math.ceil(len(document) / chunk_size)
    
    # Create the output directory if it does not exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Split the document into chunks
    chunks = [document[i:i+chunk_size] for i in range(0, len(document), chunk_size)]
    
    # Save each chunk into a separate file
    for i, chunk in enumerate(chunks):
        chunk_output_file = os.path.join(output_folder, f'chunk_{i+1}.md')
        with open(chunk_output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f'Chunk {i+1} saved to {chunk_output_file}')
    
    print(f'Total chunks created: {len(chunks)}')
    return num_chunks

def count_files(directory_path):
    """
    Count the number of files in the specified directory.
    """
    # List all files and folders in the directory
    items = os.listdir(directory_path)
    # Count only the files
    num_files = sum(os.path.isfile(os.path.join(directory_path, item)) for item in items)
    return num_files

def get_response_files():
    """
    Process all chunk files and save their combined data to an Excel file.
    """
    num_chunks_1 = count_files("chunks")
    chunks = []
    
    # Read each chunk file into a list
    for i in range(1, num_chunks_1 + 1):
        chunk_path = f"chunks/chunk_{i}.md"
        if os.path.exists(chunk_path):
            with open(chunk_path, "r", encoding="utf-8") as file:
                chunks.append(file.read())
        else:
            print(f"File {chunk_path} does not exist.")
    
    # List to store all DataFrames
    all_dataframes = []
    
    # Process each chunk and convert the response to a DataFrame
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}")
        response = pydantic_data_extractor(document=chunk)
        
        # Convert the response to a dictionary
        response_dict = json.loads(response.json())
        
        # Create a DataFrame from the properties
        df = pd.DataFrame(response_dict['properties'])
        
        print(f"Number of properties in chunk {i}: {len(df)}")
        all_dataframes.append(df)
    
    # Combine all DataFrames
    final_df = pd.concat(all_dataframes, ignore_index=True)
    
    print(f"\nTotal number of properties: {len(final_df)}")
    print("\nFirst 5 rows:")
    print(final_df.head())
    print("\nLast 5 rows:")
    print(final_df.tail())
    
    # Ensure the 'output' directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save to Excel
    output_path = os.path.join(output_dir, 'real_estate_properties.xlsx')
    final_df.to_excel(output_path, index=False)
    print(f"\nExcel file saved as '{output_path}'")
    
    # Verify the saved file
    df_verification = pd.read_excel(output_path)
    print(f"Number of rows in the Excel file: {len(df_verification)}")
    
    return output_path



# Streamlit app
st.title('Real Estate App')
st.write('This app extracts information from a real estate website and converts it into useful files.')

url = st.text_input('Enter the URL of the real estate website')

if 'num_chunks' not in st.session_state:
    st.session_state.num_chunks = 0

if st.button('Process Data'):
    # Delete previous files
    delete_files_in_directory('output')
    delete_files_in_directory('raw_data')
    delete_files_in_directory('chunks')
    st.write('Clearing...')
    
    st.write('Processing the data...')
    
    try:
        # Scrape data
        data = scrap_data(url)
        
        if not data:
            raise ValueError("No data was scraped from the URL.")
        
        # clean the data, replace every non-alphanumeric character with a space, keep commas and dots
        
        data = ''.join(e if e.isalnum() or e in [' ', ',', '.'] else ' ' for e in data)
        
         # Save raw data
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        save_raw_data(data, timestamp)
        st.write('Raw data saved.')
        
        # Save chunks and get number of chunks
        st.session_state.num_chunks = save_chunks(data)
        st.success(f'Data has been successfully processed and saved. Number of chunks: {st.session_state.num_chunks}')
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.num_chunks = 0
if st.button('Generate Files'):
    excel_file_path = get_response_files()
    st.write('Files have been generated and saved successfully.')

    # Read the Excel file
    with open(excel_file_path, "rb") as file:
        btn = st.download_button(
            label="Download Excel file",
            data=file,
            file_name="real_estate_properties.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )