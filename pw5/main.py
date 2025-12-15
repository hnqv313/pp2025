import os
import sys

import compress
import decompress
from domains.database import AutoSave, StudentMarksDatabase
from input import StudentMarksInput
from output import StudentMarksOutput


class UI(StudentMarksInput, StudentMarksOutput, StudentMarksDatabase):
    def __init__(self):
        super().__init__()
        self.__before_open()

    def __input(self):
        self._input_interface()

    def __before_open(self):
        if os.path.exists("students.dat"):
            decompress.extract_all("students.dat")
        else:
            return

        for path in AutoSave.list_paths():
            if not os.path.exists(path):
                continue

            fname = os.path.basename(path).lower()
            match fname:
                case "students.txt":
                    self.load_students(path)
                case "courses.txt":
                    self.load_courses(path)
                case "marks.txt":
                    self.load_marks(path)
                case _:
                    pass

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
                print(ValueError("Unknown option"))

    def __check_value(self):
        if not self._students or not self._courses:
            raise ValueError("Please input first")

    def __compress_menu(self):
        method: str = input("Compress method (zip, tar.gz): ").strip().lower()

        match method:
            case "zip":
                compress.zip_method()
            case "tar.gz":
                compress.tar_gz_method()
            case _:
                print("Unknown compress method")

    def __before_close(self):
        if (input("Save changes? (Y/n) ").strip().lower() or "y") == "y":
            self.__compress_menu()
        sys.exit(0)

    def main(self):
        while True:
            option: str = (
                input("Work with (input, courses, students, marks, gpa, save, exit): ")
                .strip()
                .lower()
            )

            match option:
                case "input":
                    self.__input()
                case "save":
                    self.__compress_menu()
                case "exit":
                    self.__before_close()
                case _:
                    self.__check_value()
                    self.__list(option=option)


if __name__ == "__main__":
    UI().main()
