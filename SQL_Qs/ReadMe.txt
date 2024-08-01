# Database Query App

This Streamlit application allows users to query a MySQL database using natural language questions. It utilizes LangChain and the Groq API to generate SQL queries and provide human-readable answers.

## Features

- Natural language interface for database queries
- SQL query generation using LangChain and Groq API
- Integration with MySQL database
- User-friendly Streamlit web interface

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/database-query-app.git
cd database-query-app
Copy
2. Install the required dependencies:
pip install -r requirements.txt
Copy
3. Set up your environment variables:
Create a `.env` file in the project root and add the following:
mysql_pass=your_mysql_password
groq_api_key=your_groq_api_key
Copy
## Configuration

1. Update the database connection details in the script:
```python
user = 'root'
host = 'localhost:3306'
database = 'Dhardware'

The Create_DB jupyter notebook function is to create the database out of the files in the dataset, it is up to you to configure the MySQL environment and update the credentials for the function to work. 

Usage

Run the Streamlit app:
Copystreamlit run app.py

Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).
Enter your database-related question in the text input field and click "Submit".
The app will generate an SQL query, execute it, and provide a human-readable answer based on the query results.

Dependencies

streamlit
pandas
python-dotenv
sqlalchemy
langchain-community
langchain-core
langchain-groq
mysqlclient


Author
Gilberto Gaxiola
