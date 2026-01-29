from src.infrastructure.database import get_connection
from src.response.action.mcp.schemas import (
    EnrollStudentInput,
    EnrollStudentOutput,
    RegisterGradeInput,
    RegisterGradeOutput,
)


def enroll_student(
    input_data: EnrollStudentInput,
) -> EnrollStudentOutput:
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Search student
        cur.execute(
            """
            SELECT student_id, academic_status
            FROM student
            WHERE student_name = ?
            """,
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
                message="Student is not in REGULAR academic status.",
            )

        student_id = student["student_id"]

        # 2. Search subject
        cur.execute(
            """
            SELECT subject_id
            FROM subject
            WHERE subject_name = ?
            """,
            (input_data.subject_name,),
        )
        subject = cur.fetchone()

        if subject is None:
            return EnrollStudentOutput(
                success=False,
                message="Subject not found.",
            )

        subject_id = subject["subject_id"]

        # 3. Search course for year
        cur.execute(
            """
            SELECT course_id
            FROM course
            WHERE subject_id = ?
              AND year = ?
            """,
            (subject_id, input_data.year),
        )
        course = cur.fetchone()

        if course is None:
            return EnrollStudentOutput(
                success=False,
                message="Course not found for the given year.",
            )

        course_id = course["course_id"]

        # 4. Prevent duplicate enrollment
        cur.execute(
            """
            SELECT 1
            FROM enrollment
            WHERE student_id = ?
              AND course_id = ?
            """,
            (student_id, course_id),
        )

        if cur.fetchone():
            return EnrollStudentOutput(
                success=False,
                message="Student is already enrolled in this course.",
            )

        # 5. Validate prerequisites (correlativities)
        cur.execute(
            """
            SELECT p.required_subject_id, s.subject_name
            FROM prerequisite p
            JOIN subject s ON s.subject_id = p.required_subject_id
            WHERE p.subject_id = ?
            AND p.required_subject_id NOT IN (
                SELECT c.subject_id
                FROM enrollment e
                JOIN course c ON c.course_id = e.course_id
                JOIN grade g ON g.enrollment_id = e.enrollment_id
                WHERE e.student_id = ?
                    AND g.result = 'PASSED'
            )
            """,
            (subject_id, student_id),
        )

        missing_prereqs = cur.fetchall()

        if missing_prereqs:
            missing_names = [row["subject_name"] for row in missing_prereqs]
            return EnrollStudentOutput(
                success=False,
                message=("Missing prerequisite subjects: " + ", ".join(missing_names)),
            )

        # 6. Insert enrollment
        cur.execute(
            """
            INSERT INTO enrollment (student_id, course_id, enrollment_date)
            VALUES (?, ?, DATE('now'))
            """,
            (student_id, course_id),
        )

        conn.commit()

        return EnrollStudentOutput(
            success=True,
            message=(
                f"Student {input_data.student_name} successfully enrolled "
                f"in {input_data.subject_name} ({input_data.year})."
            ),
        )

    except Exception as exc:
        conn.rollback()
        return EnrollStudentOutput(
            success=False,
            message=f"Enrollment failed due to an internal error: {exc}",
        )

    finally:
        conn.close()


def register_grade(
    input_data: RegisterGradeInput,
) -> RegisterGradeOutput:
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 0) Validate score range
        if not (0 <= input_data.score <= 10):
            return RegisterGradeOutput(
                success=False,
                message="Score must be between 0 and 10.",
            )

        # 1) Resolve student
        cur.execute(
            "SELECT student_id FROM student WHERE student_name = ?",
            (input_data.student_name,),
        )
        student = cur.fetchone()
        if student is None:
            return RegisterGradeOutput(success=False, message="Student not found.")

        # 2) Resolve subject
        cur.execute(
            "SELECT subject_id FROM subject WHERE subject_name = ?",
            (input_data.subject_name,),
        )
        subject = cur.fetchone()
        if subject is None:
            return RegisterGradeOutput(success=False, message="Subject not found.")

        # 3) Resolve course
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
            return RegisterGradeOutput(
                success=False,
                message="Course not found for the given year.",
            )

        # 4) Resolve enrollment
        cur.execute(
            """
            SELECT enrollment_id
            FROM enrollment
            WHERE student_id = ? AND course_id = ?
            """,
            (student["student_id"], course["course_id"]),
        )
        enrollment = cur.fetchone()
        if enrollment is None:
            return RegisterGradeOutput(
                success=False,
                message="Student is not enrolled in this course.",
            )

        # 5) Prevent re-grading approved enrollments
        cur.execute(
            """
            SELECT 1
            FROM grade
            WHERE enrollment_id = ?
            AND result = 'PASSED'
            """,
            (enrollment["enrollment_id"],),
        )

        if cur.fetchone():
            return RegisterGradeOutput(
                success=False,
                message="Grade already finalized as PASSED.",
            )

        # 6) Determine result
        result = "PASSED" if input_data.score >= 4 else "FAILED"

        # 7) Insert grade
        cur.execute(
            """
            INSERT INTO grade (enrollment_id, score, result, created_at)
            VALUES (?, ?, ?, DATE('now'))
            """,
            (enrollment["enrollment_id"], input_data.score, result),
        )

        conn.commit()

        return RegisterGradeOutput(
            success=True,
            message=(
                f"Grade registered: {input_data.student_name} - "
                f"{input_data.subject_name} ({input_data.year}) "
                f"Score={input_data.score} Result={result}"
            ),
        )

    except Exception as exc:
        conn.rollback()
        return RegisterGradeOutput(
            success=False,
            message=f"Failed to register grade: {exc}",
        )

    finally:
        conn.close()
