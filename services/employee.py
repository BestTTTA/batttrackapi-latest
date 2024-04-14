from fastapi import APIRouter, Body, HTTPException, Path
from modules.db import collection
from models.employee import Employee
from models.project import Project
from pymongo.collection import ReturnDocument
from entity.string_to_obj import str_to_objectid

router = APIRouter(tags=["Employee"])

# @router.post(
#     "/create_user/",
#     response_description="Add new Employee",
#     response_model=Employee,
#     status_code=status.HTTP_201_CREATED,
#     response_model_by_alias=False,
# )
# async def create_user(emp: Employee = Body(...)):
#     new_student = await collection.insert_one(emp.dict(by_alias=True, exclude={"id"}))
#     create_user = await collection.find_one({"_id": new_student.inserted_id})
#     return create_user


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
        ...,
        description="The ID of the project containing the project step to be updated",
    ),
    name_step: str = Body(
        ..., embed=True, description="The name of the project step to update"
    ),
    employee: Employee = Body(...),
):
    # Serialize the Employee object to a dictionary
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
