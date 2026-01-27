from src.infrastructure.database import get_connection


def get_student(student_name: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT student_name, academic_status
        FROM student
        WHERE student_name = ?
        """,
        (student_name,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {}

    return {
        "name": row["student_name"],
        "academic_status": row["academic_status"],
    }


def get_subject(subject_name: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT subject_name, level, term
        FROM subject
        WHERE subject_name = ?
        """,
        (subject_name,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {}

    return {
        "name": row["subject_name"],
        "level": row["level"],
        "term": row["term"],
    }


def get_passed_subjects(student_name: str) -> list[str]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT subj.subject_name
        FROM grade g
        JOIN enrollment e ON g.enrollment_id = e.enrollment_id
        JOIN course c ON e.course_id = c.course_id
        JOIN subject subj ON c.subject_id = subj.subject_id
        JOIN student st ON e.student_id = st.student_id
        WHERE st.student_name = ?
          AND g.result = 'PASSED'
        """,
        (student_name,),
    )

    rows = cur.fetchall()
    conn.close()

    return [r["subject_name"] for r in rows]


def get_current_enrollments(student_name: str) -> list[str]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT subj.subject_name
        FROM enrollment e
        JOIN course c ON e.course_id = c.course_id
        JOIN subject subj ON c.subject_id = subj.subject_id
        JOIN student st ON e.student_id = st.student_id
        WHERE st.student_name = ?
        """,
        (student_name,),
    )

    rows = cur.fetchall()
    conn.close()

    return [r["subject_name"] for r in rows]


def get_required_subjects(subject_name: str) -> list[str]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT prereq.subject_name
        FROM prerequisite p
        JOIN subject s ON p.subject_id = s.subject_id
        JOIN subject prereq ON p.required_subject_id = prereq.subject_id
        WHERE s.subject_name = ?
        """,
        (subject_name,),
    )

    rows = cur.fetchall()
    conn.close()

    return [r["subject_name"] for r in rows]
