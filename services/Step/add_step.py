from models.project_step import ProjectStep
from fastapi import APIRouter, HTTPException, Body
from modules.db import collection

router = APIRouter(tags=["Step => Add step to serial"])

@router.put("/projects/{project_name}/add_step/{serial_number}")
async def add_project_step(project_name: str, serial_number: str, project_step: ProjectStep = Body(...)):
    updated_project = await collection.find_one_and_update(
        {"name_project_head": project_name, "list_serial.serial_number": serial_number},
        {"$push": {"list_serial.$.process_step": project_step.dict()}},
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "update step success"}
