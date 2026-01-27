from typing import TypedDict, List, Dict, Any


class StudentEntity(TypedDict):
    name: str
    academic_status: str


class SubjectEntity(TypedDict):
    name: str
    level: int
    term: int


class EnrollmentEligibility(TypedDict):
    eligible: bool
    missing_prerequisites: List[str]
    reasons: List[str]


class KGContext(TypedDict):
    entities: Dict[str, Any]
    facts: Dict[str, Any]
    evaluations: Dict[str, Any]
    constraints: Dict[str, Any]
