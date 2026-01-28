from src.response.informational.kg.queries import (
    get_student,
    get_subject,
    get_passed_subjects,
    get_current_enrollments,
    get_required_subjects,
)
from src.response.informational.kg.reasoning import evaluate_enrollment
from src.response.informational.kg.types_kg import KGContext


def build_kg_context(student_name: str, subject_name: str) -> KGContext | None:
    # --- entities ---
    student = get_student(student_name)
    subject = get_subject(subject_name)
    if not student or not subject:
        return None

    # --- facts ---
    passed = set(get_passed_subjects(student_name))
    enrolled = set(get_current_enrollments(student_name))
    required = set(get_required_subjects(subject_name))

    # --- evaluations ---
    student_status = student.get("academic_status")
    if not student_status:
        student_status = "UNKNOWN"
    enrollment_eval = evaluate_enrollment(
        student_status=student_status,
        passed_subjects=passed,
        required_subjects=required,
    )

    # --- constraints (semantic identifiers) ---
    applied_rules = [
        "student_must_be_regular",
        "all_prerequisites_must_be_passed",
    ]

    violated_rules = []
    if student.get("academic_status") != "REGULAR":
        violated_rules.append("student_must_be_regular")
    if enrollment_eval["missing_prerequisites"]:
        violated_rules.append("all_prerequisites_must_be_passed")

    return {
        "entities": {
            "student": student,
            "subject": subject,
        },
        "facts": {
            "passed_subjects": sorted(passed),
            "current_enrollments": sorted(enrolled),
            "required_subjects": sorted(required),
        },
        "evaluations": {
            "enrollment_eligibility": enrollment_eval,
        },
        "constraints": {
            "applied_rules": applied_rules,
            "violated_rules": violated_rules,
        },
    }