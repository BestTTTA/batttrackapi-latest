from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from typing import Optional, List
from models.employee import Employee
from datetime import datetime


PyObjectId = Annotated[str, BeforeValidator(str)]

class ProjectStep(BaseModel):
    name_step: str
    timestart: str = "-"
    endtime: str = "-"
    process_status: bool = False
    employee: List[Employee] = []


class BreakStart(BaseModel):
    start_break: datetime

class BreakEnd(BaseModel):
    end_break: datetime