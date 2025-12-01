from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class StudentMarks:
    id: str = "0"
    name: str = "Unknown"
    DoB: datetime = field(
        default_factory=lambda: datetime.strptime("1-1-1990", "%d-%m-%Y")
    )
    marks: Dict[str, float] = field(default_factory=dict)  # key: course_id, value: mark


@dataclass
class Courses:
    id: str = "0"
    name: str = "Unknown"


class StudentMarksDatabase:
    def __init__(self):
        self._students: Dict[str, StudentMarks] = {}
        self._courses: Dict[str, Courses] = {}


class StudentMarksInput(StudentMarksDatabase):
    def __init__(self):
        super().__init__()

    def _input_student_info(self, student: StudentMarks):
        student.id = input("ID: ")
        student.name = input("Name: ")
        student.DoB = datetime.strptime(input("DoB (DD-MM-YYYY): "), "%d-%m-%Y")

    def _input_course_info(self, courses: Courses):
        courses.id = input("Course ID: ")
        courses.name = input("Course Name: ")

    def _input_info(self):
        student_number: int = int(input("Enter number of students: "))
        for _ in range(student_number):
            print()
            student = StudentMarks()
            self._input_student_info(student)
            self._students[student.id] = student

        print()
        course_number: int = int(input("Enter number of courses: "))
        for _ in range(course_number):
            print()
            course = Courses()
            self._input_course_info(courses=course)
            self._courses[course.id] = course

    def _input_marks(self):
        while True:
            print("\nAvailable courses:")
            for course in self._courses.values():
                print(f"{course.id}: {course.name}")

            course_id: str = input(
                "Select a course ID to input marks (Enter to cancel): "
            )

            if course_id.strip() == "":
                print("Cancel mark input.")
                break

            if course_id not in self._courses:
                raise ValueError("Invalid course ID!")

            print(f"\nInput marks for course: {self._courses[course_id].name}")
            for student in self._students.values():
                mark = float(input(f"Enter mark for {student.name}: "))
                student.marks[course_id] = mark

    def _input_interface(self):
        self._input_info()
        self._input_marks()


class StudentMarksOutput(StudentMarksDatabase):
    def __init__(self):
        super().__init__()

    def _list_courses(self):
        for course in self._courses.values():
            print(course.id, course.name, sep=" - ")

    def _list_students(self):
        for student in self._students.values():
            print(
                f"Name: {student.name}",
                f"ID: {student.id}",
                f"DoB: {student.DoB}",
                sep="\n",
            )

    def _show_course_student_mark(self, course_id: str):
        for student in self._students.values():
            student_mark: float | None = student.marks.get(course_id)

            if not student_mark:
                raise ValueError("Course ID not found.")

            print(student.name, student_mark, sep=": ")


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
            case _:
                raise ValueError("Unknown option")

    def __check_value(self):
        if not self._students or not self._courses:
            raise ValueError("Please input first")

    def main(self):
        while True:
            option: str = input(
                "Work with (input, courses, students, marks, exit): "
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
