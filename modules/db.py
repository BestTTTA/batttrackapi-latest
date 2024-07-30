import os
from dotenv import load_dotenv
import motor.motor_asyncio


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.batttrack
collection = db.get_collection("batttrack")