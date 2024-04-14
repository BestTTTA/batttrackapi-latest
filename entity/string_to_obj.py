from bson import ObjectId
from fastapi import HTTPException


def str_to_objectid(id: str):
    try:
        return ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid project ID format") from e
