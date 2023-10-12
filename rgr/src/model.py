from .scripts.reset_db import reset
from psycopg2 import connect


class Model:
    def __init__(self):
        self.connection = connect(
            database="students",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
        )
        self.insert_queries = {
            "students": """INSERT INTO students(name, group_id) VALUES (%s, %s)""",
            "groups": """INSERT INTO groups(name) VALUES (%s)""",
            "disciplines": """INSERT INTO disciplines(name, teacher_name) VALUES (%s, %s)""",
            "student_disciplines": """INSERT INTO student_disciplines(student_id, discipline_id) VALUES (%s, %s)""",
            "marks": """INSERT INTO marks(value, discipline_id, student_id, when_received) VALUES (%s, %s, %s, %s)""",
        }
        self.read_queries = {
            "students": "select s.name, g.name as group_name\n"
                        "from students as s\n"
                        "inner join groups as g on s.group_id = g.id",
            "groups": "select g.name as group_name\n"
                      "from groups as g",
            "disciplines": "select d.name as discipline_name, d.teacher_name as teacher_name\n"
                           "from disciplines as d",
            "marks": "select "
                     "m.value as mark_value, "
                     "s.name as student_name, "
                     "d.name as discipline_name, "
                     "m.when_received as mark_date\n"
                     "from marks as m\n"
                     "inner join students as s on m.student_id = s.id\n"
                     "inner join disciplines as d on m.discipline_id = d.id",
        }

    def disconnect(self):
        if self.connection.closed == 0:
            self.connection.close()

    def _execute_select(self, request: str) -> list:
        cur = self.connection.cursor()
        cur.execute(request)
        return cur.fetchall()

    def _execute_insert(self, where_to_insert: str, data) -> None:
        cur = self.connection.cursor()
        cur.execute(self.insert_queries[where_to_insert], data)
        self.connection.commit()
        cur.close()

    @staticmethod
    def reset_db(type_of_reset):
        reset(fill=type_of_reset)

    def create_student(self, student_name, group_name):
        group_id = self._execute_select(
            f"select g.id\n"
            f"from groups as g\n"
            f"where g.name = '{group_name}'"
        )[0][0]
        prepared_data = ((student_name, ), (group_id, ))
        self._execute_insert("students", prepared_data)

    def create_group(self, group_name):
        prepared_data = ((group_name,),)
        self._execute_insert("groups", prepared_data)

    def create_discipline(self, discipline_name, teacher_name):
        prepared_data = ((discipline_name, ), (teacher_name, ))
        self._execute_insert("disciplines", prepared_data)

    def create_mark(self, mark_value, mark_date, student_name, discipline_name):
        student_id = self._execute_select(
            f"select s.id\n"
            f"from students as s\n"
            f"where s.name = '{student_name}'"
        )[0][0]
        discipline_id = self._execute_select(
            f"select d.id\n"
            f"from disciplines as d\n"
            f"where d.name = '{discipline_name}'"
        )[0][0]
        check_if_exists = self._execute_select(
            f"select sd.student_id\n"
            f"from student_disciplines as sd\n"
            f"where sd.discipline_id = {discipline_id}")
        if len(check_if_exists) == 0:
            self._execute_insert("student_disciplines", ((student_id, ), (discipline_id, )))
        prepared_data = ((mark_value, ), (discipline_id, ), (student_id, ), (mark_date, ))
        self._execute_insert("marks", prepared_data)

    def read(self, read_from):
        result = self._execute_select(self.read_queries[read_from])
        return result


