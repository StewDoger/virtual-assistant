import os
from dotenv import load_dotenv
import motor.motor_asyncio

# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')

# Set up MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['chatbot']
products_collection = db['products']

async def get_all_products():
    """Retrieve all products from the collection."""
    products = await products_collection.find().to_list(length=None)
    return products

async def has_products():
    """Check if there are any products in the collection."""
    count = await products_collection.count_documents({})
    return count > 0