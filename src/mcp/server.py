from fastapi import FastAPI
from src.mcp.schemas import (
    EnrollStudentInput,
    EnrollStudentOutput,
    RegisterGradeInput,
    RegisterGradeOutput,
)
from src.mcp.tools import register_grade, enroll_student

app = FastAPI(title="Academic MCP Server")


@app.post("/tools/enroll_student", response_model=EnrollStudentOutput)
def enroll_student_tool(
    input_data: EnrollStudentInput,
) -> EnrollStudentOutput:
    return enroll_student(input_data)


@app.post("/tools/register_grade", response_model=RegisterGradeOutput)
def register_grade_tool(
    input_data: RegisterGradeInput,
) -> RegisterGradeOutput:
    return register_grade(input_data)
