from pydantic import BaseModel, Field


class EnrollStudentInput(BaseModel):
    student_name: str
    subject_name: str
    year: int


class EnrollStudentOutput(BaseModel):
    success: bool
    message: str


class RegisterGradeInput(BaseModel):
    student_name: str
    subject_name: str
    year: int
    score: float = Field(ge=0, le=10)


class RegisterGradeOutput(BaseModel):
    success: bool
    message: str
