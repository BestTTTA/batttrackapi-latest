from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(collection, username: str, password: str):
    user = await collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return user
    return False