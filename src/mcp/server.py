from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.mcp.db import init_db
from src.mcp.schemas import EnrollStudentInput, EnrollStudentOutput
from src.mcp.tools import enroll_student


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (si en el futuro necesitás limpiar recursos)


app = FastAPI(
    title="Academic MCP Server",
    lifespan=lifespan,
)


@app.post("/tools/enroll_student", response_model=EnrollStudentOutput)
def enroll_student_tool(
    input_data: EnrollStudentInput,
) -> EnrollStudentOutput:
    return enroll_student(input_data)
