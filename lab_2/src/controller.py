from .model import Model
from .view import View


class Controller:
    def __init__(self):
        self.available = {
            "create": {
                "db": {"reset": self.reset, "reset_fill": self.reset_fill},
                "student": self.create_student,
                "group": self.create_group,
                "discipline": self.create_discipline,
                "mark": self.create_mark,
            },
            "read": {
                "students": self.read_students,
                "groups": self.read_groups,
                "disciplines": self.read_disciplines,
                "marks": self.read_marks,
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
            if chosen_mode_viewer:
                chosen_option_viewer, chosen_option = chosen_mode_viewer()
                args_or_command = chosen_option_viewer()
            else:
                break

    def reset(self):
        pass

    def reset_fill(self):
        pass

    def create_student(self):
        pass

    def create_group(self):
        pass

    def create_discipline(self):
        pass

    def create_mark(self):
        pass

    def read_students(self):
        pass

    def read_groups(self):
        pass

    def read_disciplines(self):
        pass

    def read_marks(self):
        pass

    def update_student(self):
        pass

    def update_group(self):
        pass

    def update_discipline(self):
        pass

    def update_mark(self):
        pass

    def delete_student(self):
        pass

    def delete_group(self):
        pass

    def delete_discipline(self):
        pass

    def delete_mark(self):
        pass
