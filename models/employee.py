
from typing import List
from pydantic import BaseModel


class Break(BaseModel):
    describe: str
    start_break: str
    end_break: str

class Employee(BaseModel):
    name: str 
    list_break: List[Break] = []

