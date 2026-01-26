from src.mcp.db import get_connection
from src.mcp.schemas import EnrollStudentInput, EnrollStudentOutput


def enroll_student(
    input_data: EnrollStudentInput,
) -> EnrollStudentOutput:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO enrollment (student_name, subject_name)
        VALUES (?, ?)
        """,
        (input_data.student_name, input_data.subject_name),
    )

    conn.commit()
    conn.close()

    return EnrollStudentOutput(
        success=True,
        message=(
            f"Student {input_data.student_name} "
            f"successfully enrolled in {input_data.subject_name}."
        ),
    )
