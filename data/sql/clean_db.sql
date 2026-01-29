PRAGMA foreign_keys = ON;

-- Child tables first
DELETE FROM grade;
DELETE FROM enrollment;
DELETE FROM prerequisite;

-- Mid-level tables
DELETE FROM course;

-- Root tables
DELETE FROM subject;
DELETE FROM professor;
DELETE FROM student;

-- Reset AUTOINCREMENT counters
DELETE FROM sqlite_sequence;
