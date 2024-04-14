from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class RegisterUser(UserBase):
    password: str

class UserInDB(UserBase):
    id: str 
