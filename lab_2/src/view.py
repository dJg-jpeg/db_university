from typing import Callable, Union


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
            "db": self.show_menu_create_db,
            "student": self.show_menu_create_student,
            "group": self.show_menu_create_group,
            "discipline": self.show_menu_create_discipline,
            "mark": self.show_menu_create_mark,
        }
        self.available_read: dict = {
            "students": None,
            "groups": None,
            "disciplines": None,
            "marks": None,
        }
        self.available_update: dict = {
            "student": None,
            "group": None,
            "discipline": None,
            "mark": None
        }
        self.available_delete: dict = {
            "student": None,
            "groups": None,
            "discipline": None,
            "mark": None,
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

    def show_menu_create_db(self):
        options = {
            "reset": "reset",
            "reset_fill": "reset_fill",
        }
        self._output_options(options, amount_of_tabs=2, title="Choose type of creating/reseting db")
        return self._handle_wrong_input(options)

    @staticmethod
    def show_menu_create_student():
        student = input("Input student name:")
        print("\n")
        group = input("Input student group:")
        return student, group

    def show_menu_create_group(self):
        pass

    def show_menu_create_mark(self):
        pass

    def show_menu_create_discipline(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def show_menu_read(self):
        pass

    def show_menu_update(self):
        pass

    def show_menu_delete(self):
        pass
