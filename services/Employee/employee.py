from fastapi import APIRouter, Body, HTTPException, Path, status
from modules.db import collection
from models.employee import Employee
from models.project import Project
from pymongo.collection import ReturnDocument

router = APIRouter(tags=["Employee"])


@router.put("/projects/{project_name}/add_employee", response_model=Project)
async def add_employee(project_name: str, emp: Employee = Body(...)):
    updated_project = await collection.find_one_and_update(
        {"name_project": project_name},
        {"$push": {"employee": emp.dict()}},
        return_document=ReturnDocument.AFTER,
    )

    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")

    return Project(**updated_project)


@router.put("/projects/{project_name}/app_emp_project_step", status_code=200)
async def update_project_step_endtime(
    project_name: str = Path(
        ...
    ),
    name_step: str = Body(
        ..., embed=True
    ),
    employee: Employee = Body(...),
):
    employee_dict = employee.dict()

    result = await collection.update_one(
        {"name_project": project_name, "process_step.name_step": name_step},
        {"$push": {"process_step.$.employee": employee_dict}},
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Project not found or ProjectStep name not found"
        )

    return {"message": "ProjectStep updated successfully"}


@router.put("/employees/{emp_name}/update_name", status_code=status.HTTP_200_OK)
async def update_employee_name(
    emp_name: str = Path(...),
    new_name: str = Body(..., embed=True),
):

    result = await collection.find_one_and_update(
        {"username": emp_name},
        {"$set": {"username": new_name}},
        return_document=ReturnDocument.AFTER,
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    return
