from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from models.project_step import ProjectStep
from models.employee import Employee
from typing import Optional

PyObjectId = Annotated[str, BeforeValidator(str)]


class Project(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    serial_number: Optional[str] = None
    timestart: str = "-"
    endtime: str = "-"
    process_status: bool = False
    process_step: List[ProjectStep] = []
    # employee: List[Employee] = []


class ProjectHead(BaseModel):
    name_project_head: Optional[str] = None
    list_serial: List[Project] = []
