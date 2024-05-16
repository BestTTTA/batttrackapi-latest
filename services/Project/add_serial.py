from fastapi import APIRouter, Body, HTTPException
from modules.db import collection
from models.project import Project

router = APIRouter(tags=["Project => Add serial to project"])


@router.put("/project/add_serial/", response_model=Project)
async def AddSerial(project_name: str, project: Project = Body(...)):
    updated_project = await collection.find_one_and_update(
        {"name_project_head": project_name},
        {"$push": {"list_serial": project.dict()}},
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "add serial success"}

