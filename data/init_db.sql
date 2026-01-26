-- Motor: SQLite
-- Naming: snake_case
-- PK: INTEGER PRIMARY KEY AUTOINCREMENT
-- FK: definidas explícitamente
-- Enumeraciones: CHECK constraints
-- Fechas: TEXT (ISO 8601)
-- Normalización: 3FN

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    academic_status TEXT NOT NULL
        CHECK (academic_status IN ('REGULAR', 'FREE')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE professor (
    professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    professor_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subject (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 5),
    term INTEGER NOT NULL CHECK (term BETWEEN 1 AND 4),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    professor_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
    FOREIGN KEY (professor_id) REFERENCES professor(professor_id)
);

CREATE TABLE prerequisite (
    prerequisite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    required_subject_id INTEGER NOT NULL,

    FOREIGN KEY (subject_id) REFERENCES subject(subject_id),
    FOREIGN KEY (required_subject_id) REFERENCES subject(subject_id),

    UNIQUE (subject_id, required_subject_id)
);

CREATE TABLE enrollment (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),

    UNIQUE (student_id, course_id)
);

CREATE TABLE grade (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 10),
    result TEXT NOT NULL
        CHECK (result IN ('PASSED', 'FAILED')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (enrollment_id) REFERENCES enrollment(enrollment_id),

    UNIQUE (enrollment_id)
);

CREATE INDEX idx_student_name ON student(student_name);
CREATE INDEX idx_subject_name ON subject(subject_name);
CREATE INDEX idx_course_subject ON course(subject_id);
CREATE INDEX idx_enrollment_student ON enrollment(student_id);

