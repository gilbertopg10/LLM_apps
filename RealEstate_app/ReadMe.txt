# Real Estate Data Extraction App

## Description
This Streamlit application scrapes real estate data from a given website, processes it, and converts it into a structured Excel file. It uses the Groq LLM model for data extraction and provides a user-friendly interface for inputting URLs and downloading the resulting data.

## Features
- Web scraping of real estate listings
- Data cleaning and preprocessing
- Chunking of large datasets for efficient processing
- LLM-based information extraction using Groq's llama-3.1-70b-versatile model
- Conversion of extracted data into a structured Excel file
- Streamlit-based user interface for easy interaction

## Installation

1. Clone this repository:
git clone [your-repo-url]
2. Install the required dependencies:
pip install -r requirements.txt
3. Set up your Groq API key as an environment variable:
export groq_apikey=your_api_key_here


#Usage

1. Run the Streamlit app:

streamlit run app.py


2. Open the provided URL in your web browser.

3. Enter the URL of the real estate website you want to scrape.

4. Click on "Process Data" to scrape and preprocess the data.

5. Click on "Generate Files" to extract information and create the Excel file.

6. Download the generated Excel file using the "Download Excel file" button.

## Project Structure
- `app.py`: Main Streamlit application file
- `chunks/`: Directory for storing chunked data
- `raw_data/`: Directory for storing raw scraped data
- `output/`: Directory for storing the final Excel file

## Dependencies
- Streamlit
- Pandas
- Pydantic
- Groq
- LLMTextCompletionProgram (custom or third-party library)

## Notes
- Ensure you have the necessary permissions to scrape data from the target website.
- The app uses the Groq LLM model, which requires an API key.
- Large datasets are processed in chunks to manage memory usage efficiently.

