import os
import psycopg2
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv('.env')

# Configure logging
logging.basicConfig(
    filename='data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

# Removing duplicates
def remove_duplicates(table_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            DELETE FROM {table_name}
            WHERE ctid NOT IN (
                SELECT MIN(ctid)
                FROM {table_name}
                GROUP BY message_id
            );
            ''')
            conn.commit()
            logging.info(f"Duplicates removed from {table_name}")
    except Exception as e:
        logging.error(f"Error removing duplicates from {table_name}: {e}")

# Handling missing values and standardizing formats
def clean_data(table_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            UPDATE {table_name}
            SET message = COALESCE(message, 'No message available'),
                date = COALESCE(date, NOW()) -- Set missing dates to the current date
            WHERE message IS NULL OR date IS NULL;
            ''')
            conn.commit()
            logging.info(f"Missing values handled and data standardized for {table_name}")
    except Exception as e:
        logging.error(f"Error cleaning data in {table_name}: {e}")

# Data validation
def validate_data(table_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            SELECT COUNT(*) FROM {table_name}
            WHERE message IS NOT NULL AND date IS NOT NULL;
            ''')
            result = cursor.fetchone()
            logging.info(f"Validated {result[0]} records in {table_name}")
            print(f"Validated {result[0]} records in {table_name}")
    except Exception as e:
        logging.error(f"Error validating data in {table_name}: {e}")

# Main function to execute all steps
def main():
    table_name = os.getenv('DB_NAME')  # Replace with your table name
    logging.info(f"Starting data cleaning process for {table_name}")
    remove_duplicates(table_name)
    clean_data(table_name)
    validate_data(table_name)
    logging.info(f"Data cleaning process completed for {table_name}")

if __name__ == "__main__":
    main()
