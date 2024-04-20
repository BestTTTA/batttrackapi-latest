from models.project import Project
from models.project_step import ProjectStep, BreakStart, BreakEnd
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


@router.put("/projects/{project_name}/steps/{name_step}/start_break", status_code=200)
async def start_break(
    project_name: str = Path(..., description="The ID of the project containing the project step to update"),
    name_step: str = Path(..., description="The name of the project step to start break"),
    break_start: BreakStart = Body(..., embed=True)
):
    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$set": {"process_step.$.start_break": break_start.start_break}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    return {"message": "Break start time recorded successfully"}

@router.put("/projects/{project_name}/steps/{name_step}/end_break", status_code=200)
async def end_break(
    project_name: str = Path(..., description="The ID of the project containing the project step to update"),
    name_step: str = Path(..., description="The name of the project step to end break"),
    break_end: BreakEnd = Body(..., embed=True)
):
    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$set": {"process_step.$.end_break": break_end.end_break}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    return {"message": "Break end time recorded successfully"}

@router.get("/projects/{project_name}/steps/{name_step}/get_break_duration", status_code=200)
async def get_break_duration(
    project_name: str = Path(..., description="The ID of the project containing the project step to query"),
    name_step: str = Path(..., description="The name of the project step to get break duration for")
):
    project_step = await collection.find_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"process_step.$": 1}
    )
    if not project_step:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    start_break = project_step['process_step'][0]['start_break']
    end_break = project_step['process_step'][0]['end_break']

    if not start_break or not end_break:
        raise HTTPException(status_code=400, detail="Break start or end time not recorded")

    duration_seconds = (end_break - start_break).total_seconds()
    return {
        "message": "Break duration retrieved successfully",
        "break_duration_minutes": duration_seconds / 60
    }