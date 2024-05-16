from fastapi import APIRouter, HTTPException, Path
from modules.db import collection

router = APIRouter(tags=["Step => Update start step"])

@router.put("/projects/{name_project_head}/{serial_number}/{name_step}/{timestart}/update_project_step_start", status_code=200)
async def start(
    timestart: str,
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
                "list_serial.$[serial].process_step.$[step].timestart": timestart
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
