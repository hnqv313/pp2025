from input import StudentMarksInput
from output import StudentMarksOutput


class UI(StudentMarksInput, StudentMarksOutput):
    def __init__(self):
        super().__init__()

    def __input(self):
        self._input_interface()

    def __list(self, option: str | None = None):
        match option:
            case "courses":
                self._list_courses()
            case "students":
                self._list_students()
            case "marks":
                self._show_course_student_mark(input("Course ID: "))
            case "gpa":
                self._list_students_by_gpa()
            case "save":
                self.export_to_json()
            case "pickle_save":
                self.export_to_pickle()
            case _:
                print(ValueError("Unknown option"))

    def __check_value(self):
        if not self._students or not self._courses:
            raise ValueError("Please input first")

    def main(self):
        while True:
            option: str = input(
                "Work with (input, "
                "courses, students, marks, gpa, "
                "save, load, pickle_save, pickle_load, exit): "
            ).lower()

            match option:
                case "input":
                    self.__input()
                case "load":
                    self.import_from_json()
                case "pickle_load":
                    self.import_from_pickle()
                case "exit":
                    if (
                        input(
                            "The unsaved data in this session be lost, exit? (y/N) "
                        ).lower()
                        == "y"
                    ):
                        break
                case _:
                    self.__check_value()

                    self.__list(option=option)


if __name__ == "__main__":
    UI().main()
