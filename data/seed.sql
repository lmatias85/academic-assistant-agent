PRAGMA foreign_keys = ON;

-- Initial Data for the database

-- Students
INSERT INTO student (student_name, academic_status)
VALUES
  ('John Doe', 'REGULAR'),
  ('Jane Smith', 'REGULAR'),
  ('Mark Brown', 'FREE');

-- Professors
INSERT INTO professor (professor_name)
VALUES
  ('Dr. Albert Newton'),
  ('Dr. Marie Curie');

-- Subjects
INSERT INTO subject (subject_name, level, term)
VALUES
  ('Math I', 1, 1),
  ('Physics I', 1, 2),
  ('Physics II', 2, 1);

-- Courses (year = 2025)
INSERT INTO course (subject_id, professor_id, year)
VALUES
  ((SELECT subject_id FROM subject WHERE subject_name = 'Math I'),
   (SELECT professor_id FROM professor WHERE professor_name = 'Dr. Albert Newton'),
   2025),

  ((SELECT subject_id FROM subject WHERE subject_name = 'Physics I'),
   (SELECT professor_id FROM professor WHERE professor_name = 'Dr. Marie Curie'),
   2025),

  ((SELECT subject_id FROM subject WHERE subject_name = 'Physics II'),
   (SELECT professor_id FROM professor WHERE professor_name = 'Dr. Marie Curie'),
   2025);

-- Prerequisites
INSERT INTO prerequisite (subject_id, required_subject_id)
VALUES
  (
    (SELECT subject_id FROM subject WHERE subject_name = 'Physics II'),
    (SELECT subject_id FROM subject WHERE subject_name = 'Physics I')
  ),
  (
    (SELECT subject_id FROM subject WHERE subject_name = 'Physics I'),
    (SELECT subject_id FROM subject WHERE subject_name = 'Math I')
  );

-- Enrollments
INSERT INTO enrollment (student_id, course_id)
VALUES
  (
    (SELECT student_id FROM student WHERE student_name = 'John Doe'),
    (SELECT course_id FROM course
     WHERE subject_id = (SELECT subject_id FROM subject WHERE subject_name = 'Math I')
       AND year = 2025)
  ),
  (
    (SELECT student_id FROM student WHERE student_name = 'Jane Smith'),
    (SELECT course_id FROM course
     WHERE subject_id = (SELECT subject_id FROM subject WHERE subject_name = 'Physics I')
       AND year = 2025)
  );

-- Grades
INSERT INTO grade (enrollment_id, score, result)
VALUES
  (
    (SELECT enrollment_id FROM enrollment
     WHERE student_id = (SELECT student_id FROM student WHERE student_name = 'John Doe')),
    8.0,
    'PASSED'
  );
