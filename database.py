import os
from dotenv import load_dotenv
import motor.motor_asyncio  # Pastikan menggunakan motor untuk async MongoDB

# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB URI from environment variables
mongo_uri = os.getenv('MONGO_URI')

# Set up MongoDB async client (Motor)
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = client.chatbot
products_collection = db['products']

async def get_all_products():
    """Retrieve all products from the collection asynchronously."""
    try:
        # Menggunakan to_list() untuk hasil query asinkron
        products = await products_collection.find().to_list(length=None)
        return products
    except Exception as e:
        print(f"Error while fetching products: {e}")
        return []