from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from modules.db import collection
from entity.login import authenticate_user

router = APIRouter(tags=["Login"], responses={404: {"description": "Not Found"}})

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(collection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return {"username": user["username"]}
