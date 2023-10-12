DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name CHAR(5) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name CHAR(50) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

DROP TABLE IF EXISTS disciplines CASCADE;
CREATE TABLE disciplines (
    id SERIAL PRIMARY KEY,
    name CHAR(50) UNIQUE NOT NULL,
    teacher_name CHAR(50) NOT NULL
);

DROP TABLE IF EXISTS student_disciplines;
CREATE TABLE student_disciplines (
    student_id INTEGER,
    discipline_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (discipline_id) REFERENCES disciplines (id)
);

DROP TABLE IF EXISTS marks;
CREATE TABLE marks (
    value SMALLINT NOT NULL,
    discipline_id INTEGER,
    student_id INTEGER,
    when_received DATE NOT NULL,
    FOREIGN KEY(discipline_id) REFERENCES disciplines (id),
    FOREIGN KEY(student_id) REFERENCES students (id)
);