from fastapi import APIRouter, HTTPException,Query
from modules.db import collection
from models.project import ProjectHead 
from bson import json_util
import json
from typing import List, Optional
from models.searchall import ProjectHead

router = APIRouter(tags=["Project => Search"])


def project_to_model(project) -> Optional[ProjectHead]:
    project.pop("_id", None)
    try:
        return ProjectHead(**project)
    except Exception:
        return None

@router.get("/projects", response_model=List[ProjectHead])
async def get_all_projects():
    projects = await collection.find().to_list(length=None)
    valid_projects = [project_to_model(project) for project in projects if project_to_model(project)]
    if valid_projects:
        return valid_projects
    else:
        raise HTTPException(status_code=404, detail="No projects found")

@router.get("/search_project_name/{project_name}") 
async def get_project_by_name(project_name: str):
    projects = await collection.find({"name_project_head": project_name}).to_list(length=None)
    if projects:
        return [ProjectHead(**project) for project in projects]
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("/search_project_details/{serial_number}")
async def get_project_details(serial_number: str):
    # Query to find a project that contains the serial number in its list_serial array
    query = {"list_serial.serial_number": serial_number}
    project = await collection.find_one(query)
    
    if project:
        # Extract the list_serial part where the serial number matches
        for serial in project.get("list_serial", []):
            if serial["serial_number"] == serial_number:
                # Convert the part of document to JSON and then back to dict for proper serialization
                serial_json = json.loads(json_util.dumps(serial))
                return serial_json
        raise HTTPException(status_code=404, detail="Serial number not found in the given project")
    else:
        raise HTTPException(status_code=404, detail="Project not found")
    

@router.get("/search_step_details/{name_project_head}/{serial_number}/{name_step}")
async def get_step_details(name_project_head: str, serial_number: str, name_step: str):
    # Query to find a project that matches both the project head name and the serial number
    query = {"name_project_head": name_project_head, "list_serial.serial_number": serial_number}
    project = await collection.find_one(query)
    
    if project:
        # Extract the list_serial part where the serial number matches
        for serial in project.get("list_serial", []):
            if serial["serial_number"] == serial_number:
                # Extract the process_step where the name_step matches
                for step in serial.get("process_step", []):
                    if step["name_step"] == name_step:
                        # Convert the part of document to JSON and then back to dict for proper serialization
                        step_json = json.loads(json_util.dumps(step))
                        return step_json
                raise HTTPException(status_code=404, detail="Step name not found in the given serial")
        raise HTTPException(status_code=404, detail="Serial number not found in the given project")
    else:
        raise HTTPException(status_code=404, detail="Project not found")
    
    
@router.get("/search_by_employee_work_not_done/{employee_name}")
async def get_projects_by_employee_status(employee_name: str):
    # This query assumes the structure of your documents and the logic needs to be confirmed against actual data.
    # It searches for projects where any serial or step has a false status and includes the specified employee.
    query = {
        "$and": [
            {"list_serial.process_status": False}, 
            {"list_serial.process_step": {
                "$elemMatch": {
                    "process_status": False, 
                    "employee": {
                        "$elemMatch": {
                            "name": employee_name
                        }
                    }
                }
            }}
        ]
    }
    projects = await collection.find(query).to_list(length=None)

    if projects:
        # Convert MongoDB documents to JSON and then back to dict for response
        projects_json = json.loads(json_util.dumps(projects))
        return projects_json
    else:
        raise HTTPException(status_code=404, detail="No projects found matching the criteria")
    
    
@router.get("/search_by_employee_work_done/{employee_name}")
async def get_projects_by_employee_status(employee_name: str):
    # This query assumes the structure of your documents and the logic needs to be confirmed against actual data.
    # It searches for projects where any serial or step has a false status and includes the specified employee.
    query = {
        "$and": [
            {"list_serial.process_status": True}, 
            {"list_serial.process_step": {
                "$elemMatch": {
                    "process_status": True, 
                    "employee": {
                        "$elemMatch": {
                            "name": employee_name
                        }
                    }
                }
            }}
        ]
    }
    projects = await collection.find(query).to_list(length=None)

    if projects:
        # Convert MongoDB documents to JSON and then back to dict for response
        projects_json = json.loads(json_util.dumps(projects))
        return projects_json
    else:
        raise HTTPException(status_code=404, detail="No projects found matching the criteria")
    
# New route to search for projects by serial number and get the project name
@router.get("/search_project_by_serial/{serial_number}")
async def get_project_name_by_serial(serial_number: str):
    query = {"list_serial.serial_number": serial_number}
    project = await collection.find_one(query)
    
    if project:
        # Return the project name
        return {"project_name": project["name_project_head"]}
    else:
        raise HTTPException(status_code=404, detail="Project not found")
