from typing import Callable, Union
from datetime import datetime


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
            "marks": self.show_read_disciplines,
        }
        self.available_update: dict = {
            "student": self.show_update_students,
            "group": self.show_update_groups,
            "discipline": self.show_update_disciplines,
            "mark": self.show_update_marks,
        }
        self.available_delete: dict = {
            "student": self.show_delete_students,
            "groups": self.show_delete_groups,
            "discipline": self.show_delete_disciplines,
            "mark": self.show_delete_marks,
        }

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
            if len(group) > 4:
                print("\nPlease input group name that fits in 4 characters\n")
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

    def show_read_students(self):
        pass

    def show_read_groups(self):
        pass

    def show_read_disciplines(self):
        pass

    def show_read_marks(self):
        pass

    def show_menu_update(self):
        self._output_options(
            self.available_update,
            amount_of_tabs=1,
            title="Choose what do you want to update"
        )
        response = self._handle_wrong_input(self.available_update)
        return response, self._get_key_by_value(self.available_update, response)

    def show_update_students(self):
        pass

    def show_update_groups(self):
        pass

    def show_update_disciplines(self):
        pass

    def show_update_marks(self):
        pass

    def show_menu_delete(self):
        self._output_options(
            self.available_delete,
            amount_of_tabs=1,
            title="Choose what do you want to read"
        )
        response = self._handle_wrong_input(self.available_delete)
        return response, self._get_key_by_value(self.available_delete, response)

    def show_delete_students(self):
        pass

    def show_delete_groups(self):
        pass

    def show_delete_disciplines(self):
        pass

    def show_delete_marks(self):
        pass
