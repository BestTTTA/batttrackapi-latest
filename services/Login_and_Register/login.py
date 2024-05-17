from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from modules.db import collection
from entity.login import authenticate_user
from models.user import RegisterUser
from bson import ObjectId

router = APIRouter(tags=["Login"], responses={404: {"description": "Not Found"}})

@router.post("/login/", response_model=RegisterUser)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(collection, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    resuser = await collection.find_one({"username": form_data.username})
    if not resuser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Ensure to return the user information in the correct format
    return resuser
