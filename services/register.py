from fastapi import APIRouter, HTTPException, status
from modules.db import collection
from models.user import RegisterUser
from entity.register import get_password_hash

router = APIRouter(tags=["Register"])

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user_create: RegisterUser):
    existing_user = await collection.find_one({"username": user_create.username})
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Username {user_create.username} already exists")
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.dict()
    user_data['password'] = hashed_password
    result = await collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "username": user_create.username}
