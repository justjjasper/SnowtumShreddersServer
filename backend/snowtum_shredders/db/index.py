# Import modules
import os
from dotenv import load_dotenv
import psycopg2

# Load environmental variables
load_dotenv()

# Define database connection parameters
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_PORT = os.getenv('PG_PORT')


# Database connection parameters
db_params = {
  'dbname': PG_DATABASE,
  'user': PG_USER,
  'password': PG_PASSWORD,
  'host': PG_HOST,
  'port': PG_PORT,
}

# Connection to database
conn = psycopg2.connect(**db_params)
