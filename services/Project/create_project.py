from fastapi import APIRouter, status, Body, HTTPException
from modules.db import collection
from models.project import ProjectHead

router = APIRouter(tags=["Project => Create Project Head"])

@router.post("/project/create_project_head/", response_model=ProjectHead, status_code=status.HTTP_201_CREATED)
async def create_project_head(projecthead: ProjectHead = Body(...)):
    existing_project = await collection.find_one({"name_project_head": projecthead.name_project_head})
    if existing_project:
        raise HTTPException(status_code=400, detail=f"Project Head with name '{projecthead.name_project_head}' already exists.")
    await collection.insert_one(projecthead.dict(by_alias=True, exclude={"id"}))
    
    return {"message": "Create Project Head success"}
