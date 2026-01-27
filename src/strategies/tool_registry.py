from typing import Callable, Dict

from src.mcp.client import (
    enroll_student_via_mcp,
    register_grade_via_mcp,
)
from src.mcp.schemas import (
    EnrollStudentInput,
    RegisterGradeInput,
)

ToolHandler = Callable[[dict], str]


def _enroll_student_handler(args: dict) -> str:
    data = EnrollStudentInput(**args)
    result = enroll_student_via_mcp(data)
    return result.message


def _register_grade_handler(args: dict) -> str:
    data = RegisterGradeInput(**args)
    result = register_grade_via_mcp(data)
    return result.message


TOOL_REGISTRY: Dict[str, ToolHandler] = {
    "enroll_student": _enroll_student_handler,
    "register_grade": _register_grade_handler,
}
