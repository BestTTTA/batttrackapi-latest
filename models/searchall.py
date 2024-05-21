from typing import List, Optional
from pydantic import BaseModel


class Break(BaseModel):
    describe: Optional[str]
    start_break: Optional[str]
    end_break: Optional[str]

class Employee(BaseModel):
    name: Optional[str]
    list_break: Optional[List[Break]]

class ProcessStep(BaseModel):
    name_step: Optional[str]
    timestart: Optional[str]
    endtime: Optional[str]
    process_status: Optional[bool]
    employee: Optional[List[Employee]]

class Serial(BaseModel):
    serial_number: Optional[str]
    timestart: Optional[str]
    endtime: Optional[str]
    process_status: Optional[bool]
    process_step: Optional[List[ProcessStep]]

class ProjectHead(BaseModel):
    name_project_head: Optional[str]
    list_serial: Optional[List[Serial]]