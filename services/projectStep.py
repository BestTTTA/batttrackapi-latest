from models.project import Project
from models.project_step import ProjectStep
from fastapi import APIRouter, HTTPException, Body, Path
from modules.db import collection
from bson import ObjectId
from pymongo.collection import ReturnDocument

router = APIRouter(tags=["ProjectStep"])


def str_to_objectid(id: str):
    try:
        return ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid project ID format") from e


@router.put("/projects/{project_name}/add_step", response_model=Project)
async def add_project_step(project_name: str, project_step: ProjectStep = Body(...)):
    updated_project = await collection.find_one_and_update(
        {"name_project": project_name},
        {"$push": {"process_step": project_step.dict()}},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project(**updated_project)


@router.put("/projects/{project_name}/update_project_step_timestart", status_code=200)
async def update_project_step_timestart(
    project_name: str = Path(..., description="The ID of the project containing the project step to be updated"),
    name_step: str = Body(..., embed=True, description="The name of the project step to update"),
    new_timestart: str = Body(..., embed=True, description="The new timestart value for the project step")
):
    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$set": {"process_step.$.timestart": new_timestart}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or ProjectStep name not found")
    updated_project = await collection.find_one({"name_project": project_name}, {"process_step": 1, "_id": 0})
    return {"updated_project_step": [step for step in updated_project['process_step'] if step['name_step'] == name_step]}


@router.put("/projects/{project_name}/update_project_step_endtime", status_code=200)
async def update_project_step_endtime(
    project_name: str = Path(..., description="The ID of the project containing the project step to be updated"),
    name_step: str = Body(..., embed=True, description="The name of the project step to update"),
    new_endtime: str = Body(..., embed=True, description="The new endtime value for the project step")
):

    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$set": {"process_step.$.endtime": new_endtime}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or ProjectStep name not found")

    return {"message": "ProjectStep endtime updated successfully"}


@router.put("/projects/{project_name}/update_project_step_status", status_code=200)
async def update_project_step_status(
    project_name: str = Path(..., description="The ID of the project containing the project step to be updated"),
    name_step: str = Body(..., embed=True, description="The name of the project step to update"),
    new_status: bool = Body(..., embed=True, description="The new process status for the project step")
):

    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$set": {"process_step.$.process_status": new_status}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or ProjectStep name not found")

    return {"message": "ProjectStep process_status updated successfully"}
