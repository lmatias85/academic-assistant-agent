from pydantic import BaseModel
from typing import Optional


class InformationalEntities(BaseModel):
    student_name: Optional[str] = None
    subject_name: Optional[str] = None
