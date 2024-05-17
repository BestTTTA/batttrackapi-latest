from fastapi import APIRouter, HTTPException, status
from modules.db import collection
from models.user import RegisterUser
from entity.register import get_password_hash

router = APIRouter(tags=["Register"])

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user_create: RegisterUser):
    # Check if the username already exists
    existing_user = await collection.find_one({"username": user_create.username})
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Username {user_create.username} already exists")

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create a user dict, replacing the plaintext password with the hashed one
    user_data = user_create.dict()
    user_data['password'] = hashed_password

    # Insert the new user into the database
    await collection.insert_one(user_data)

    # Return the username and picture URL, confirming the registration
    return {"username": user_create.username, "picture_url": user_create.picture_url}
