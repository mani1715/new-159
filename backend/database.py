from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Collections
users_collection = db['users']
page_content_collection = db['page_content']
services_collection = db['services']
projects_collection = db['projects']
contacts_collection = db['contacts']
settings_collection = db['settings']
admins_collection = db['admins']
storage_collection = db['storage']
skills_collection = db['skills']
content_collection = db['content']
notes_collection = db['notes']
contact_page_collection = db['contact_page']
conversations_collection = db['conversations']
blogs_collection = db['blogs']
testimonials_collection = db['testimonials']
newsletter_collection = db['newsletter']
pricing_collection = db['pricing']
analytics_collection = db['analytics']
# Client Portal Collections
clients_collection = db['clients']
client_projects_collection = db['client_projects']
# Booking Collections
bookings_collection = db['bookings']
booking_settings_collection = db['booking_settings']

async def close_db_connection():
    client.close()
