from pydantic import BaseModel

class RegisterUser(BaseModel):
    username: str
    password: str
    picture_url: str
