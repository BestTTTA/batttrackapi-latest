from fastapi import APIRouter, HTTPException, Path
from modules.db import collection

router = APIRouter(tags=["Step => Update end break"])

@router.put("/projects/{name_project_head}/{serial_number}/{name_step}/{describe}/{emp_name}/{endtime}/update_endbreak", status_code=200)
async def end_break(
    endtime: str,
    describe: str,
    emp_name: str,
    name_project_head: str = Path(...),
    serial_number: str = Path(...),
    name_step: str = Path(...)
):
    result = await collection.find_one_and_update(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
            "list_serial.process_step.name_step": name_step,
            "list_serial.process_step.employee.name": emp_name,
            "list_serial.process_step.employee.list_break.describe": describe
        },
        {
            "$set": {
                "list_serial.$[serial].process_step.$[step].employee.$[emp].list_break.$[brk].end_break": endtime
            }
        },
        array_filters=[
            {"serial.serial_number": serial_number},
            {"step.name_step": name_step},
            {"emp.name": emp_name},
            {"brk.describe": describe} 
        ]
    )

    if not result:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    return {"message": "Break successfully updated"}
