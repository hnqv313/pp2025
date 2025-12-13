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
            case _:
                raise ValueError("Unknown option")

    def __check_value(self):
        if not self._students or not self._courses:
            raise ValueError("Please input first")

    def main(self):
        while True:
            option: str = input(
                "Work with (input, courses, students, marks, gpa, exit): "
            ).lower()

            match option:
                case "input":
                    self.__input()
                case "exit":
                    if (
                        input("The data in this session be lost, exit? (y/N) ").lower()
                        == "y"
                    ):
                        break
                case _:
                    self.__check_value()

                    self.__list(option=option)


if __name__ == "__main__":
    UI().main()
