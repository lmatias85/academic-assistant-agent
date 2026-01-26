from src.mcp.db import get_connection
from src.mcp.schemas import EnrollStudentInput, EnrollStudentOutput


def enroll_student(
    input_data: EnrollStudentInput,
) -> EnrollStudentOutput:
    conn = get_connection()
    cur = conn.cursor()

    # 1. Search student
    cur.execute(
        "SELECT student_id, academic_status FROM student WHERE student_name = ?",
        (input_data.student_name,),
    )
    student = cur.fetchone()

    if student is None:
        return EnrollStudentOutput(
            success=False,
            message="Student not found.",
        )

    if student["academic_status"] != "REGULAR":
        return EnrollStudentOutput(
            success=False,
            message="Student is not in REGULAR status.",
        )

    # 2. Search subject
    cur.execute(
        "SELECT subject_id FROM subject WHERE subject_name = ?",
        (input_data.subject_name,),
    )
    subject = cur.fetchone()

    if subject is None:
        return EnrollStudentOutput(
            success=False,
            message="Subject not found.",
        )

    # 3. Search course for year
    cur.execute(
        """
        SELECT course_id
        FROM course
        WHERE subject_id = ? AND year = ?
        """,
        (subject["subject_id"], input_data.year),
    )
    course = cur.fetchone()

    if course is None:
        return EnrollStudentOutput(
            success=False,
            message="Course not found for the given year.",
        )

    # 4. Insert enrollment
    try:
        cur.execute(
            """
            INSERT INTO enrollment (student_id, course_id)
            VALUES (?, ?)
            """,
            (student["student_id"], course["course_id"]),
        )
        conn.commit()
    except Exception:
        return EnrollStudentOutput(
            success=False,
            message="Student is already enrolled in this course.",
        )
    finally:
        conn.close()

    return EnrollStudentOutput(
        success=True,
        message=(
            f"Student {input_data.student_name} successfully enrolled "
            f"in {input_data.subject_name} ({input_data.year})."
        ),
    )
