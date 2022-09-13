from typing import List
from pydantic import BaseModel 

class Course(BaseModel):
    ccode : str
    cname : str
    credits : int
    ltpj : List[int] = []

class Faculty(BaseModel):
    emp_id : str
    name : str
    desig : str
    phno : str
    school : str
    email : str
    pref : List[str] = []

class Wish(BaseModel):
    ccode : str
    cname : str
    nwish : int
    nbatches : int

