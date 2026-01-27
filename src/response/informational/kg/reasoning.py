def evaluate_enrollment(
    *,
    student_status: str,
    passed_subjects: set[str],
    required_subjects: set[str],
) -> dict:
    missing = sorted(required_subjects - passed_subjects)
    reasons: list[str] = []

    if student_status != "REGULAR":
        reasons.append(f"Student academic status is {student_status}")

    if missing:
        reasons.append(f"Missing prerequisite subjects: {', '.join(missing)}")

    return {
        "eligible": len(reasons) == 0,
        "missing_prerequisites": missing,
        "reasons": reasons,
    }
