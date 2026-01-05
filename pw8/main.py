import os
import sys
import threading

import compress
import decompress
from domains.database import AutoSave, StudentMarksDatabase
from input import StudentMarksInput
from output import StudentMarksOutput


class UI(StudentMarksInput, StudentMarksOutput, StudentMarksDatabase):
    def __init__(self):
        super().__init__()
        self.save_thread: threading.Thread | None = None
        self.load_thread: threading.Thread | None = None
        self.__before_open()

    def __input(self):
        self._input_interface()

    def __load_data_thread(self):
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

    def __before_open(self):
        print("Loading data in background...")
        self.load_thread = threading.Thread(target=self.__load_data_thread)
        self.load_thread.daemon = True
        self.load_thread.start()

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
        self.__ensure_data_loaded()

        if not self._students or not self._courses:
            raise ValueError("Please input first")

    def __compress_thread(self, method):
        match method:
            case "zip":
                compress.zip_method()
            case "tar.gz":
                compress.tar_gz_method()
            case _:
                print("Unknown compress method")

    def __compress_menu(self):
        if self.save_thread is not None and self.save_thread.is_alive():
            print("\n[Warning] Background save is still running! Please wait.")
            return None

        method: str = input("Compress method (zip, tar.gz): ").strip().lower()

        self.save_thread = threading.Thread(
            target=self.__compress_thread, args=(method,)
        )
        self.save_thread.start()

        return self.save_thread

    def __before_close(self):
        if (input("Save changes? (Y/n) ").strip().lower() or "y") == "y":
            self.__ensure_data_loaded()

            t = self.__compress_menu()

            if t is not None:
                print("Saving... Please wait...")
                t.join()
            elif self.save_thread is not None and self.save_thread.is_alive():
                print("Finishing background save task... Please wait...")
                self.save_thread.join()

        sys.exit(0)

    def __ensure_data_loaded(self):
        if self.load_thread is not None and self.load_thread.is_alive():
            print("Data is still loading... Please wait a moment...")
            self.load_thread.join()
            print("Done waiting. Executing command...")

    def main(self):
        while True:
            option: str = (
                input("Work with (input, courses, students, marks, gpa, save, exit): ")
                .strip()
                .lower()
            )

            match option:
                case "input":
                    self.__ensure_data_loaded()
                    self.__input()
                case "save":
                    self.__ensure_data_loaded()
                    self.__compress_menu()
                case "exit":
                    self.__before_close()
                case _:
                    self.__check_value()
                    self.__list(option=option)


if __name__ == "__main__":
    UI().main()
