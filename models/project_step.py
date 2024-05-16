from pydantic import BaseModel
from typing import List
from models.employee import Employee


class ProjectStep(BaseModel):
    name_step: str
    timestart: str = "-"
    endtime: str = "-"
    process_status: bool = False
    employee: List[Employee] = []
