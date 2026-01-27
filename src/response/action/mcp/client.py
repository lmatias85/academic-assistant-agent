import requests

from src.response.action.config import MCP_BASE_URL
from src.response.action.mcp.schemas import (
    EnrollStudentInput,
    EnrollStudentOutput,
    RegisterGradeInput,
    RegisterGradeOutput,
)


def enroll_student_via_mcp(
    data: EnrollStudentInput,
) -> EnrollStudentOutput:
    url = f"{MCP_BASE_URL}/tools/enroll_student"
    response = requests.post(
        url,
        json=data.model_dump(),
        timeout=5,
    )
    response.raise_for_status()
    return EnrollStudentOutput(**response.json())


def register_grade_via_mcp(
    data: RegisterGradeInput,
) -> RegisterGradeOutput:
    url = f"{MCP_BASE_URL}/tools/register_grade"
    response = requests.post(url, json=data.model_dump(), timeout=5)
    response.raise_for_status()
    return RegisterGradeOutput(**response.json())
