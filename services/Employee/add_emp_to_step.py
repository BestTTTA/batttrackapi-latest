from fastapi import APIRouter, Body, HTTPException, Path
from modules.db import collection
from models.employee import Employee

router = APIRouter(tags=["Employee => Add emp to step"])


@router.put(
    "/projects/{name_project_head}/{serial_number}/app_emp_project_step",
    status_code=200,
)
async def add_emp_step(
    name_project_head: str,
    serial_number: str,
    name_step: str,
    employee: Employee = Body(...),
):
    result = await collection.find_one_and_update(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
            "list_serial.process_step.name_step": name_step,
        },
        {
            "$push": {
                "list_serial.$[serial].process_step.$[step].employee": employee.dict()
            }
        },
        array_filters=[
            {"serial.serial_number": serial_number},
            {"step.name_step": name_step},
        ],
    )

    if not result:
        raise HTTPException(
            status_code=404, detail="Project not found or ProjectStep name not found"
        )

    return {"message": "updated successfully"}
