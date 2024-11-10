import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://wiradinataa9:wdinata33@data.etzoacx.mongodb.net/')
db = client['chatbot']
products_collection = db['products']

async def get_all_products():
    # Retrieve all products from the collection
    products = await products_collection.find().to_list(length=None)
    return products