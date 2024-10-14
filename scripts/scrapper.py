from telethon import TelegramClient
import os
import psycopg2
from dotenv import load_dotenv
import logging
import asyncio

# Load environment variables once
load_dotenv('.env')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL database setup
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Function to create table if it doesn't exist
def create_table(channel_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {channel_name} (
            message_id SERIAL PRIMARY KEY,
            channel_title VARCHAR(255),
            channel_username VARCHAR(255),
            sender_id BIGINT,
            date TIMESTAMP,
            message TEXT,
            media_path VARCHAR(255)
        )
        ''')
        conn.commit()

# Function to insert data into the database
def insert_data(channel_name, data):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {channel_name} (channel_title, channel_username, sender_id, date, message, media_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    create_table(channel_username.replace('@', ''))  # Ensure the table exists (removing @ for table names)

    async for message in client.iter_messages(entity, limit=10000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a directory for the channel's photos
            os.makedirs(f'photos/{channel_username}', exist_ok=True)
            # Create a unique filename for the photo
            filename = f"{message.id}.jpg"
            media_path = os.path.join(f'photos/{channel_username}', filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Prepare the data for insertion
        data = (channel_title, channel_username, message.sender_id, message.date, message.text, media_path)
        
        try:
            insert_data(channel_username.replace('@', ''), data)  # Insert data into the database
            logging.info(f"Inserted message {message.id} into database from {channel_username}")
        except Exception as e:
            logging.error(f"Error inserting message {message.id} from {channel_username}: {e}")

# Initialize the client once
client = TelegramClient('kara_solutions_session', API_ID, API_HASH)

async def main():
    await client.start()

    # Create a directory for media files
    os.makedirs('photos', exist_ok=True)

    # List of channels to scrape (include all required channels for image scraping and data collection)
    channels = [
        '@DoctorsET',              # Medical business channel
        '@lobelia4cosmetics',       # For object detection
        'CheMed123',  # For object detection (replace with actual username)
    ]

    # Iterate over channels and scrape data into the database
    for channel in channels:
        await scrape_channel(client, channel)
        logging.info(f"Scraped data from {channel}")

# Start the client and run the main coroutine
async def run():
    async with client:
        await main()

# Check if we're in an async context (like Jupyter)
try:
    asyncio.get_event_loop().run_until_complete(run())
except RuntimeError:  # Already running
    asyncio.ensure_future(run())
