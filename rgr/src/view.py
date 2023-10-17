from typing import Callable, Union
from datetime import datetime
from tabulate import tabulate


class View:

    def __init__(self):
        self.available_commands_menus: dict = {
            "create": self.show_menu_create,
            "read": self.show_menu_read,
            "update": self.show_menu_update,
            "delete": self.show_menu_delete,
            "quit": None,
        }
        self.available_create: dict = {
            "db": self.show_create_db,
            "student": self.show_create_student,
            "group": self.show_create_group,
            "discipline": self.show_create_discipline,
            "mark": self.show_create_mark,
        }
        self.available_read: dict = {
            "students": self.show_read_students,
            "groups": self.show_read_groups,
            "disciplines": self.show_read_disciplines,
            "marks": self.show_read_marks,
        }
        self.available_update: dict = {
            "student": self.show_update_students,
            "group": self.show_update_groups,
            "discipline": self.show_update_disciplines,
            "mark": self.show_update_marks,
        }
        self.available_delete: dict = {
            "student": self.show_delete_student,
            "groups": self.show_delete_group,
            "discipline": self.show_delete_discipline,
            "mark": self.show_delete_mark,
        }
        self.table_headers: dict = {
            "students": ("student_name", "group_name"),
            "groups": ("group_name", ),
            "disciplines": ("discipline_name", "teacher_name"),
            "marks": ("mark_value", "student_name", "discipline_name", "mark_date"),
        }

    def output_table(self, table, table_name):
        print("\n\n")
        print(
            tabulate(
                [[field.strip() if type(field) is str else field for field in row] for row in table],
                headers=self.table_headers[table_name]
            )
        )

    @staticmethod
    def output_error_message():
        print("Incorrect input")

    @staticmethod
    def _output_options(options_dict: dict, amount_of_tabs: int, title: str) -> None:
        options = tuple(options_dict.keys())
        tab_string = "\t" * amount_of_tabs
        print(f"\n\n{tab_string}{title}:\n")
        for index, option in enumerate(options):
            print(f"{tab_string}{index + 1}. {option}\n")

    @staticmethod
    def _handle_wrong_input(options: dict) -> Union[Callable, str]:
        while True:
            try:
                keys = tuple(options.keys())
                option = keys[int(input("Input number of the option: ").strip()) - 1]
                return options[option]
            except (IndexError, ValueError):
                print("No such option, try again")

    @staticmethod
    def _get_key_by_value(dct: dict, value):
        keys = tuple(dct.keys())
        values = tuple(dct.values())
        index = values.index(value)
        return keys[index]

    def show_menu(self) -> tuple[Callable, str]:
        self._output_options(
            self.available_commands_menus,
            amount_of_tabs=0,
            title="Choose one option from the options given below"
        )
        response = self._handle_wrong_input(self.available_commands_menus)
        return response, self._get_key_by_value(self.available_commands_menus, response)

    def show_menu_create(self) -> tuple[Callable, str]:
        self._output_options(
            self.available_create,
            amount_of_tabs=1,
            title="Choose what do you want to create"
        )
        response = self._handle_wrong_input(self.available_create)
        return response, self._get_key_by_value(self.available_create, response)

    def show_create_db(self):
        options = {
            "reset": "reset",
            "reset_fill": "reset_fill",
        }
        self._output_options(options, amount_of_tabs=2, title="Choose type of creating/reseting db")
        return self._handle_wrong_input(options)

    @staticmethod
    def show_create_student():
        while True:
            student = input("Input student name:")
            if len(student) > 50:
                print("\nPlease input student name that fits in 50 characters\n")
                continue
            else:
                break
        print("\n")
        group = input("Input student group:")
        return student, group

    @staticmethod
    def show_create_group():
        while True:
            group = input("Input group name:")
            if len(group) > 5:
                print("\nPlease input group name that fits in 5 characters\n")
                continue
            return group

    @staticmethod
    def show_create_mark():
        student_name = input("Input name of person, who received this mark:")
        discipline_name = input("Input discipline name:")
        while True:
            try:
                mark = int(input("Input mark:"))
                assert 1 <= mark <= 12
                when_received = datetime.strptime(input("Input when mark was received:"), "%d.%m.%Y").date()
                return mark, when_received, student_name, discipline_name
            except (ValueError, AssertionError):
                print("Please input correct value")

    @staticmethod
    def show_create_discipline():
        while True:
            discipline_name = input("Input name of the discipline:")
            if len(discipline_name) > 50:
                print("\nPlease input discipline name that fits in 50 characters\n")
                continue
            teacher_name = input("Input teacher name:")
            if len(teacher_name) > 50:
                print("\nPlease input teacher name that fits in 50 characters\n")
                continue
            return discipline_name, teacher_name

    def show_menu_read(self):
        self._output_options(
            self.available_read,
            amount_of_tabs=1,
            title="Choose what do you want to read"
        )
        response = self._handle_wrong_input(self.available_read)
        return response, self._get_key_by_value(self.available_read, response)

    @staticmethod
    def show_read_students():
        return "students"

    @staticmethod
    def show_read_groups():
        return "groups"

    @staticmethod
    def show_read_disciplines():
        return "disciplines"

    @staticmethod
    def show_read_marks():
        return "marks"

    def show_menu_update(self):
        self._output_options(
            self.available_update,
            amount_of_tabs=1,
            title="Choose what do you want to update"
        )
        response = self._handle_wrong_input(self.available_update)
        return response, self._get_key_by_value(self.available_update, response)

    def show_update_students(self):
        while True:
            student = input("Input student name:")
            if len(student) > 50:
                print("\nPlease input student name that fits in 50 characters\n")
                continue
            else:
                break
        change_options = {"change_name": "name", "change_group": "group_id"}
        self._output_options(
            change_options,
            amount_of_tabs=2,
            title="Choose what do you want to change"
        )
        response = self._handle_wrong_input(change_options)
        new_value = input("\nInput new value:")
        return student, response, new_value

    @staticmethod
    def show_update_groups():
        while True:
            group = input("Input group name:")
            if len(group) > 5:
                print("\nPlease input group name that fits in 5 characters\n")
                continue
            else:
                break
        new_value = input("\nInput new value:")
        return group, new_value

    def show_update_disciplines(self):
        while True:
            discipline_name = input("Input name of the discipline:")
            if len(discipline_name) > 50:
                print("\nPlease input discipline name that fits in 50 characters\n")
                continue
            else:
                break
        change_options = {"change_discipline_name": "name", "change_teacher_name": "teacher_name"}
        self._output_options(
            change_options,
            amount_of_tabs=2,
            title="Choose what do you want to change"
        )
        response = self._handle_wrong_input(change_options)
        new_value = input("\nInput new value:")
        return discipline_name, response, new_value

    def show_update_marks(self):
        student_name = input("Input name of person, who received this mark:")
        discipline_name = input("Input discipline name:")
        change_options = {"change_mark_value": "value", "change_mark_date": "when_received"}
        self._output_options(
            change_options,
            amount_of_tabs=2,
            title="Choose what do you want to change"
        )
        response = self._handle_wrong_input(change_options)
        new_value = input("\nInput new value:")
        return student_name, discipline_name, response, new_value

    def show_menu_delete(self):
        self._output_options(
            self.available_delete,
            amount_of_tabs=1,
            title="Choose what do you want to delete"
        )
        response = self._handle_wrong_input(self.available_delete)
        return response, self._get_key_by_value(self.available_delete, response)

    @staticmethod
    def show_delete_student():
        while True:
            student = input("Input student name:")
            if len(student) > 50:
                print("\nPlease input student name that fits in 50 characters\n")
                continue
            return student

    @staticmethod
    def show_delete_group():
        while True:
            group = input("Input group name:")
            if len(group) > 5:
                print("\nPlease input group name that fits in 5 characters\n")
                continue
            return group

    @staticmethod
    def show_delete_discipline():
        while True:
            discipline = input("Input discipline name:")
            if len(discipline) > 50:
                print("\nPlease input discipline name that fits in 50 characters\n")
                continue
            return discipline

    @staticmethod
    def show_delete_mark():
        student_name = input("Input name of person, who received this mark:")
        discipline_name = input("Input discipline name:")
        return student_name, discipline_name
