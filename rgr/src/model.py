from .scripts.reset_db import reset
from psycopg2 import connect
from datetime import datetime


class Model:
    def __init__(self):
        self.connection = connect(
            database="students",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
        )
        self.get_id_queries = {
            "student": "select s.id\n"
                       "from students as s\n"
                       "where s.name = '{}'",
            "group": "select g.id\n"
                     "from groups as g\n"
                     "where g.name = '{}'",
            "discipline": "select d.id\n"
                          "from disciplines as d\n"
                          "where d.name = '{}'",
        }
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

        self.request_queries = {
            "student_rating": "SELECT ROUND(AVG(m.value), 2) as avg_mark, s.name\n"
                              "FROM marks as m\n"
                              "INNER JOIN students as s ON m.student_id = s.id\n"
                              "GROUP BY s.id\n"
                              "ORDER BY avg_mark DESC",
            "avg_group_discipline_mark": "SELECT ROUND(AVG(m.value), 2) as average_mark, "
                                         "g.name as group_name, d.name as discipline_name\n"
                                         "FROM marks as m\n"
                                         "INNER JOIN students as s ON m.student_id = s.id\n"
                                         "INNER JOIN disciplines as d ON m.discipline_id = d.id\n"
                                         "INNER JOIN groups as g ON s.group_id = g.id\n"
                                         "GROUP BY d.name, g.name\n"
                                         "ORDER BY g.name",
            "student_group_list": "SELECT s.name as student_name, g.name as group_name\n"
                                  "FROM students as s\n"
                                  "INNER JOIN groups as g ON s.group_id = g.id\n"
                                  "WHERE g.id = {}\n",
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

    def _execute_query(self, query: str) -> None:
        cur = self.connection.cursor()
        cur.execute(query)
        self.connection.commit()
        cur.close()

    def reset_db(self, type_of_reset):
        reset(type_of_reset, self.connection)

    def request_rating(self):
        return self._execute_select(self.request_queries["student_rating"])

    def request_avg_mark(self):
        return self._execute_select(self.request_queries["avg_group_discipline_mark"])

    def request_group_list(self, group_name):
        group_id = self._execute_select(self.get_id_queries["group"].format(group_name))[0][0]
        return self._execute_select(self.request_queries["student_group_list"].format(group_id))

    def create_student(self, student_name, group_name):
        group_id = self._execute_select(self.get_id_queries["group"].format(group_name))[0][0]
        prepared_data = ((student_name,), (group_id,))
        self._execute_insert("students", prepared_data)

    def create_group(self, group_name):
        prepared_data = ((group_name,),)
        self._execute_insert("groups", prepared_data)

    def create_discipline(self, discipline_name, teacher_name):
        prepared_data = ((discipline_name,), (teacher_name,))
        self._execute_insert("disciplines", prepared_data)

    def create_mark(self, mark_value, mark_date, student_name, discipline_name):
        student_id = self._execute_select(self.get_id_queries["student"].format(student_name))[0][0]
        discipline_id = self._execute_select(self.get_id_queries["discipline"].format(discipline_name))[0][0]
        check_if_exists = self._execute_select(
            f"select sd.student_id\n"
            f"from student_disciplines as sd\n"
            f"where sd.discipline_id = {discipline_id}")
        if len(check_if_exists) == 0:
            self._execute_insert("student_disciplines", ((student_id,), (discipline_id,)))
        prepared_data = ((mark_value,), (discipline_id,), (student_id,), (mark_date,))
        self._execute_insert("marks", prepared_data)

    def read(self, read_from):
        result = self._execute_select(self.read_queries[read_from])
        return result

    def update_student(self, find_name, what_to_change, new_value):
        student_id = self._execute_select(self.get_id_queries["student"].format(find_name))[0][0]
        value_to_set = new_value
        if what_to_change == "group_id":
            group_name = new_value
            value_to_set = self._execute_select(
                f"select g.id\n"
                f"from groups as g\n"
                f"where g.name = '{group_name}'"
            )[0][0]
        self._execute_query(
            f"update students\n"
            f"set {what_to_change} = '{value_to_set}'\n"
            f"where id = {student_id};"
        )

    def update_group(self, find_name, new_value):
        group_id = self._execute_select(self.get_id_queries["group"].format(find_name))[0][0]
        self._execute_query(
            f"update groups\n"
            f"set name = '{new_value}'\n"
            f"where id = {group_id};"
        )

    def update_discipline(self, find_name, what_to_change, new_value):
        discipline_id = self._execute_select(self.get_id_queries["discipline"].format(find_name))[0][0]
        self._execute_query(
            f"update disciplines\n"
            f"set {what_to_change} = '{new_value}'\n"
            f"where id = {discipline_id};"
        )

    def update_mark(self, find_student, find_discipline, what_to_change, new_value):
        student_id = self._execute_select(self.get_id_queries["student"].format(find_student))[0][0]
        discipline_id = self._execute_select(self.get_id_queries["discipline"].format(find_discipline))[0][0]
        if what_to_change == "value":
            assert 1 <= int(new_value) <= 12
        elif what_to_change == "when_received":
            new_value = datetime.strptime(new_value, "%d.%m.%Y").date()

        self._execute_query(
            f"update marks\n"
            f"set {what_to_change} = '{new_value}'\n"
            f"where student_id = '{student_id}' and discipline_id = '{discipline_id}'"
        )

    def delete_student(self, name):
        student_id = self._execute_select(self.get_id_queries["student"].format(name))[0][0]

        query = f"delete from student_disciplines where student_id = {student_id};\n" \
                f"delete from marks where student_id = {student_id};\n" \
                f"delete from students where id = {student_id};"
        self._execute_query(query)

    def delete_group(self, name):
        group_id = self._execute_select(self.get_id_queries["group"].format(name))[0][0]
        students = self._execute_select(
            f"select s.name\n"
            f"from students as s\n"
            f"where s.group_id = '{group_id}'"
        )
        students = [student[0].strip() for student in students]
        for s_name in students:
            self.delete_student(s_name)

        self._execute_query(f"delete from groups where id = {group_id}")

    def delete_discipline(self, name):
        discipline_id = self._execute_select(self.get_id_queries["discipline"].format(name))[0][0]

        query = f"delete from student_disciplines where discipline_id = {discipline_id};\n" \
                f"delete from marks where discipline_id = {discipline_id};\n" \
                f"delete from disciplines where id = {discipline_id};"
        self._execute_query(query)

    def delete_mark(self, find_student, find_discipline):
        student_id = self._execute_select(self.get_id_queries["student"].format(find_student))[0][0]
        discipline_id = self._execute_select(self.get_id_queries["discipline"].format(find_discipline))[0][0]

        query = \
            f"delete from student_disciplines where student_id = {student_id} and discipline_id = {discipline_id};\n" \
            f"delete from marks where student_id = {student_id} and discipline_id = {discipline_id};"
        self._execute_query(query)
