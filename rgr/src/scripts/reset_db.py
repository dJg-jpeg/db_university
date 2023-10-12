from datetime import date
from faker import Faker
from random import randint, choice
from psycopg2 import connect
from pathlib import Path

STUDENTS_AMOUNT = 6
GROUPS_AMOUNT = 3
DISCIPLINES_AMOUNT = 5
TEACHERS_AMOUNT = 3
EACH_STUDENT_MARKS_AMOUNT = 5
choose_discipline = [
    'Physics',
    'English',
    'Programming',
    'Data Structures and Algorithms',
    'Computer Logic',
    'Math Analysis',
    'History of science and technology',
    'Discrete Math',
    'Analytical geometry and linear algebra',
]


def create() -> None:
    filepath = Path(__file__).parent.resolve() / Path("all_marks.sql")
    with open(filepath, 'r') as file:
        scrypt = file.read()

    connection = connect(
        database="students",
        user="admin",
        password="admin",
        host="127.0.0.1",
        port="5432",
    )

    with connection.cursor() as cur:
        cur.execute(scrypt)

    cur.close()
    connection.commit()
    connection.close()


def generate_data() -> tuple[list, list, list, list, list[list, list]]:
    student_names = []
    group_names = []
    discipline_names = []
    teachers_names = []
    marks_and_dates = [[], []]
    fake_data = Faker('uk_UA')

    for _ in range(STUDENTS_AMOUNT):
        student_names.append(fake_data.name())

    for _ in range(TEACHERS_AMOUNT):
        teachers_names.append(fake_data.name())

    for _ in range(GROUPS_AMOUNT):
        group_names.append(fake_data.bothify(text='??-##'))

    for _ in range(DISCIPLINES_AMOUNT):
        discipline = choice(choose_discipline)
        discipline_names.append(discipline)
        choose_discipline.remove(discipline)

    for _ in range(EACH_STUDENT_MARKS_AMOUNT * STUDENTS_AMOUNT):
        marks_and_dates[0].append(randint(1, 12))
        marks_and_dates[1].append(
            fake_data.date_between(
                start_date=date(year=2023, month=1, day=5),
                end_date=date(year=2023, month=1, day=20),
            )
        )

    return student_names, group_names, discipline_names, teachers_names, marks_and_dates


def prepare_data(student_names, group_names, discipline_names, teachers_names, marks_and_dates) -> tuple:
    prepared_groups = []
    for group in group_names:
        prepared_groups.append((group,))

    prepared_students = []
    for student in student_names:
        prepared_students.append((student, randint(1, GROUPS_AMOUNT)))

    prepared_disciplines = []
    for discipline in discipline_names:
        prepared_disciplines.append((discipline, choice(teachers_names)))

    prepared_discipline_student_relationships = []
    for student_id in range(1, STUDENTS_AMOUNT + 1):
        disciplines_ids = list(range(1, DISCIPLINES_AMOUNT + 1))
        for d_id in disciplines_ids:
            prepared_discipline_student_relationships.append((student_id, d_id))

    prepared_marks = []
    discipline_student_marks_relationships_dict = {}
    for student_id in range(1, STUDENTS_AMOUNT + 1):
        discipline_student_marks_relationships_dict[student_id] = []
    for student_discipline_ids in prepared_discipline_student_relationships:
        discipline_student_marks_relationships_dict[
            student_discipline_ids[0]
        ].append(student_discipline_ids)
    for student, discipline in discipline_student_marks_relationships_dict.items():
        for d_id in discipline:
            mark = marks_and_dates[0].pop(0)
            mark_date = marks_and_dates[1].pop(0)
            prepared_marks.append((mark, d_id[1], student, mark_date))

    return (
        prepared_students,
        prepared_groups,
        prepared_disciplines,
        prepared_discipline_student_relationships,
        prepared_marks,
    )


def insert_data_to_db(students_table, groups_table, disciplines_table, student_disciplines_table, marks_table) -> None:
    with connect(
            database="students",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
    ) as connection:
        cur = connection.cursor()

        sql_to_groups = """INSERT INTO groups(name) VALUES (%s)"""
        cur.executemany(sql_to_groups, groups_table)

        sql_to_students = """INSERT INTO students(name, group_id) VALUES (%s, %s)"""
        cur.executemany(sql_to_students, students_table)

        sql_to_disciplines = """INSERT INTO disciplines(name, teacher_name) VALUES (%s, %s)"""
        cur.executemany(sql_to_disciplines, disciplines_table)

        sql_to_student_disciplines = """INSERT INTO student_disciplines(student_id, discipline_id) VALUES (%s, %s)"""
        cur.executemany(sql_to_student_disciplines, student_disciplines_table)

        sql_to_marks = """INSERT INTO marks(value, discipline_id, student_id, when_received) VALUES (%s, %s, %s, %s)"""
        cur.executemany(sql_to_marks, marks_table)

        connection.commit()
        cur.close()
    connection.close()


def reset(fill) -> None:
    create()
    if fill:
        students, groups, disciplines, teachers, marks = generate_data()
        for_students, for_groups, for_disciplines, for_student_disciplines, for_marks = prepare_data(
            students,
            groups,
            disciplines,
            teachers,
            marks
        )
        insert_data_to_db(for_students, for_groups, for_disciplines, for_student_disciplines, for_marks)
