from fastapi import APIRouter, status, Body, HTTPException, Path
from modules.db import collection


router = APIRouter(tags=["Project => Project Update Status"])


@router.put(
    "/projects/{name_project_head}/{serial_number}/update_status",
    status_code=status.HTTP_200_OK,
)
async def update_project_status(
    name_project_head: str = Path(...),
    serial_number: str = Path(...),
    process_status: bool = Body(..., embed=True),
):
    result = await collection.find_one_and_update(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
        },
        {"$set": {"list_serial.$.process_status": process_status}},
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "update serial status success"}
