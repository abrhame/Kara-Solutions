import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Removing duplicates
def remove_duplicates(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        DELETE FROM {table_name}
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM {table_name}
            GROUP BY message_id
        );
        ''')
        conn.commit()

# Handling missing values and standardizing formats
def clean_data(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        UPDATE {table_name}
        SET message = COALESCE(message, 'No message available'),
            date = COALESCE(date, NOW()) -- Example: setting missing dates to the current date
        WHERE message IS NULL OR date IS NULL;
        ''')
        conn.commit()

# Data validation
def validate_data(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        SELECT COUNT(*) FROM {table_name}
        WHERE message IS NOT NULL AND date IS NOT NULL;
        ''')
        result = cursor.fetchone()
        print(f"Validated {result[0]} records")
