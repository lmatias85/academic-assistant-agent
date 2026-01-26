from src.mcp.db import get_connection


def fetch_prerequisites() -> list[tuple[str, str]]:
    """
    Returns (subject_name, required_subject_name)
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.subject_name, rs.subject_name
        FROM prerequisite p
        JOIN subject s ON p.subject_id = s.subject_id
        JOIN subject rs ON p.required_subject_id = rs.subject_id
        """)

    rows = cur.fetchall()
    conn.close()
    return [(r[0], r[1]) for r in rows]


def fetch_passed_subjects(student_name: str) -> list[str]:
    """
    Subjects PASSED by a student.
    """
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
    return [r[0] for r in rows]
