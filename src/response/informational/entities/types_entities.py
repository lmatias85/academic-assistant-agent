from pydantic import BaseModel
from typing import Optional


class AcademicEntities(BaseModel):
    student_name: Optional[str] = None
    professor_name: Optional[str] = None
    subject_name: Optional[str] = None
    course_name: Optional[str] = None

    mentions_enrollment: bool = False
    mentions_grade: bool = False
    mentions_prerequisite: bool = False

    def is_academic(self) -> bool:
        return any(
            [
                self.student_name,
                self.professor_name,
                self.subject_name,
                self.course_name,
                self.mentions_enrollment,
                self.mentions_grade,
                self.mentions_prerequisite,
            ]
        )