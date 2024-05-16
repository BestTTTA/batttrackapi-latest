from fastapi import APIRouter, status, HTTPException, Path, UploadFile, File
from modules.db import collection
router = APIRouter(tags=["Project => Project Update time end"])


@router.put(
    "/projects/{name_project_head}/{serial_number}/end_process/{endtime}",
    status_code=status.HTTP_200_OK,
)
async def end_project_process(
    name_project_head: str = Path(...), serial_number: str = Path(...), endtime=str
):
    result = await collection.update_one(
        {
            "name_project_head": name_project_head,
            "list_serial.serial_number": serial_number,
        },
        {"$set": {"list_serial.$.endtime": endtime}},
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Project not found or no update made"
        )
    return {"message": "update endtime success"}

