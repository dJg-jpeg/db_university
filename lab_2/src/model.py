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
            "disciplines": None,
            "marks": None,
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
        group_id = self._execute_select(f"select g.id\n"
                                        f"from groups as g\n"
                                        f"where g.name = '{group_name}'")[0][0]
        prepared_data = ((student_name, group_id),)
        self._execute_insert("students", prepared_data)

    def create_group(self, group_name):
        prepared_data = ((group_name,),)
        self._execute_insert("groups", prepared_data)
