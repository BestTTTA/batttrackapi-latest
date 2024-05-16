from fastapi import APIRouter, status, HTTPException, Path
from modules.db import collection

router = APIRouter(tags=["Project => Project Update time start"])


@router.put(
    "/projects/{name_project_head}/{serial_number}/start_process/{timestart}",  
    status_code=status.HTTP_200_OK,
)
async def start_project_process(
    name_project_head: str = Path(...),
    serial_number: str = Path(...),
    timestart = str
):
    result = await collection.update_one(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
        },
        {"$set": {"list_serial.$.timestart": timestart}},
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Project not found or no update made"
        )
    return {"message": "update starttime success"}
