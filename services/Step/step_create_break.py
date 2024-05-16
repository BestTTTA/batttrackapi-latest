from fastapi import APIRouter, HTTPException, Path, Body
from modules.db import collection
from models.employee import Break  

router = APIRouter(tags=["Step => Update create break"])

@router.put("/projects/{name_project_head}/{serial_number}/{name_step}/{emp_name}/create_break", status_code=200)
async def create_break(
    name_project_head: str = Path(...),
    serial_number: str = Path(...),
    name_step: str = Path(...),
    emp_name: str = Path(...),
    break_body: Break = Body(...)
):
    result = await collection.find_one_and_update(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
            "list_serial.process_step.name_step": name_step,
            "list_serial.process_step.employee.name": emp_name
        },
        {
            "$push": {
                "list_serial.$[serial].process_step.$[step].employee.$[emp].list_break": break_body.dict()
            }
        },
        array_filters=[
            {"serial.serial_number": serial_number},
            {"step.name_step": name_step},
            {"emp.name": emp_name}
        ]
    )

    if not result:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    return {"message": "Break successfully created"}
