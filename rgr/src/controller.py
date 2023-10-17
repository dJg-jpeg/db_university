from .model import Model
from .view import View
from functools import wraps
from psycopg2.errors import StringDataRightTruncation


def catch_db_error(option):
    @wraps(option)
    def inner(self, *args, **kwargs):
        try:
            option(self, *args, **kwargs)
        except (IndexError, StringDataRightTruncation, ValueError, AssertionError):
            self.view.output_error_message()

    return inner


class Controller:
    def __init__(self):
        self.available = {
            "create": {
                "db": self.reset,
                "student": self.create_student,
                "group": self.create_group,
                "discipline": self.create_discipline,
                "mark": self.create_mark,
            },
            "read": {
                "students": self.read,
                "groups": self.read,
                "disciplines": self.read,
                "marks": self.read,
            },
            "update": {
                "student": self.update_student,
                "group": self.update_group,
                "discipline": self.update_discipline,
                "mark": self.update_mark,
            },
            "delete": {
                "student": self.delete_student,
                "groups": self.delete_group,
                "discipline": self.delete_discipline,
                "mark": self.delete_mark,
            },
        }
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            chosen_mode_viewer, chosen_mode = self.view.show_menu()
            if not chosen_mode_viewer:
                self.model.disconnect()
                break
            chosen_option_viewer, chosen_option = chosen_mode_viewer()
            args_or_command = chosen_option_viewer()
            self.available[chosen_mode][chosen_option](args_or_command)

    def reset(self, type_of_reset):
        if type_of_reset == "reset_fill":
            self.model.reset_db(True)
        else:
            self.model.reset_db(False)

    @catch_db_error
    def create_student(self, args):
        name, group_name = args
        self.model.create_student(name, group_name)

    def create_group(self, name):
        self.model.create_group(name)

    def create_discipline(self, args):
        name, teacher_name = args
        self.model.create_discipline(name, teacher_name)

    @catch_db_error
    def create_mark(self, args):
        value, mark_date, student_name, discipline_name = args
        self.model.create_mark(value, mark_date, student_name, discipline_name)

    def read(self, read_from):
        table = self.model.read(read_from)
        self.view.output_table(table, read_from)

    @catch_db_error
    def update_student(self, args):
        name, what_to_change, new_value = args
        self.model.update_student(name, what_to_change, new_value)

    @catch_db_error
    def update_group(self, args):
        name, new_value = args
        self.model.update_group(name, new_value)

    @catch_db_error
    def update_discipline(self, args):
        find_name, what_to_change, new_value = args
        self.model.update_discipline(find_name, what_to_change, new_value)

    @catch_db_error
    def update_mark(self, args):
        find_student, find_discipline, what_to_change, new_value = args
        self.model.update_mark(find_student, find_discipline, what_to_change, new_value)

    @catch_db_error
    def delete_student(self, name):
        self.model.delete_student(name)

    @catch_db_error
    def delete_group(self, name):
        self.model.delete_group(name)

    @catch_db_error
    def delete_discipline(self, name):
        self.model.delete_discipline(name)

    @catch_db_error
    def delete_mark(self, args):
        student, discipline = args
        self.model.delete_mark(student, discipline)
