from fastapi import APIRouter, HTTPException, Path, Body
from modules.db import collection

router = APIRouter(tags=["Step => Update status step"])

@router.put("/projects/{name_project_head}/{serial_number}/{name_step}/update_project_step_status", status_code=200)
async def status(
    process_status: bool = Body(..., embed=True),
    name_project_head: str = Path(...),
    serial_number: str = Path(...),
    name_step: str = Path(...)
):
    result = await collection.find_one_and_update(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
            "list_serial.process_step.name_step": name_step,
        },
        {
            "$set": {
                "list_serial.$[serial].process_step.$[step].process_status": process_status
            }
        },
        array_filters=[
            {"serial.serial_number": serial_number},
            {"step.name_step": name_step},
        ]
    )

    if not result:
        raise HTTPException(status_code=404, detail="Project or project step not found")

    return {"message": "successfully updated"}
