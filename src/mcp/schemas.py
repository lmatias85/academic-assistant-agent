from pydantic import BaseModel


class EnrollStudentInput(BaseModel):
    student_name: str
    subject_name: str


class EnrollStudentOutput(BaseModel):
    success: bool
    message: str
