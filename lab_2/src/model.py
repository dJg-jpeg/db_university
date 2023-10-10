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

    def disconnect(self):
        if self.connection.closed == 0:
            self.connection.close()

    def _execute_request(self, request: str) -> list:
        cur = self.connection.cursor()
        cur.execute(request)
        return cur.fetchall()

    @staticmethod
    def reset_db(type_of_reset):
        reset(fill=type_of_reset)

    def create_student(self, student_name, group_name):
        group_id = self._execute_request(
            f"select g.id\n"
            f"from groups as g\n"
            f"where g.name = '{group_name}'"
        )[0][0]
        query = """INSERT INTO students(name, group_id) VALUES (%s, %s)"""
        prepared_data = ((student_name, group_id),)
        cur = self.connection.cursor()
        cur.execute(query, prepared_data)
        self.connection.commit()
        cur.close()

