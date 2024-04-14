from fastapi import APIRouter, status, Body, HTTPException, Path
from modules.db import collection
from models.project import Project
from typing import List
from pymongo import ReturnDocument
from entity.string_to_obj import str_to_objectid

router = APIRouter(tags=["Project"])

@router.post("/create_project/", response_description="Add new Project", response_model=Project, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_project(project: Project = Body(...)):
    # Check if a project with the same name already exists
    existing_project = await collection.find_one({"name_project": project.name_project})
    if existing_project:
        raise HTTPException(status_code=400, detail=f"Project with name '{project.name_project}' already exists.")
    
    # Proceed to create a new project since it doesn't exist
    new_project = await collection.insert_one(project.dict(by_alias=True, exclude={"id"}))
    create_project = await collection.find_one({"_id": new_project.inserted_id})
    
    return create_project


@router.get("/search_project_name/{project_name}", response_model=Project, response_description="Get a project by name")
async def get_project_by_name(project_name: str = Path(..., description="The name of the project to get")):
    # Query the database for the project by name
    project = await collection.find_one({"name_project": project_name})
    
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("/projects", response_model=List[Project])
async def get_all_projects():
    projects = await collection.find().to_list(length=None)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return [Project(**project) for project in projects]

@router.put("/projects/{project_name}/timestart", response_model=Project, status_code=status.HTTP_200_OK)
async def update_project_timestart(project_name: str = Path(..., description="The name of the project to be updated"), 
                                    timestart: str = Body(..., embed=True)):
    # Query and update the document based on project name
    result = await collection.update_one({"name_project": project_name}, {"$set": {"timestart": timestart}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or timestart is the same")
    updated_project = await collection.find_one({"name_project": project_name})
    return Project(**updated_project)

@router.put("/projects/{project_name}/end_process", response_model=Project, status_code=status.HTTP_200_OK)
async def end_project_process(project_name: str = Path(..., description="The ID of the project to update its end process"), endtime: str = Body(..., embed=True)):
    result = await collection.update_one({"name_project": project_name}, {"$set": {"endtime": endtime, "process_status": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or no update made")
    updated_project = await collection.find_one({"name_project": project_name})
    return Project(**updated_project)


@router.put("/projects/{project_id}/update_status", response_model=Project, status_code=status.HTTP_200_OK)
async def update_project_status(project_id: str = Path(..., description="The ID of the project to be updated"), 
                                process_status: bool = Body(..., embed=True)):
    project_id_obj = str_to_objectid(project_id) 
    result = await collection.find_one_and_update(
        {"_id": project_id_obj},
        {"$set": {"process_status": process_status}},
        return_document=ReturnDocument.AFTER
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return Project(**result)