import math
from datetime import datetime

from domains.course import Courses
from domains.database import StudentMarksDatabase
from domains.student import StudentMarks


class StudentMarksInput(StudentMarksDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _input_student_info(self, student: StudentMarks):
        student.id = input("ID: ")
        student.name = input("Name: ")
        student.DoB = datetime.strptime(input("DoB (DD-MM-YYYY): "), "%d-%m-%Y")

    def _input_course_info(self, courses: Courses):
        courses.id = input("Course ID: ")
        courses.name = input("Course Name: ")
        courses.credits = int(input("Credits: "))

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
                mark = (
                    math.floor(float(input(f"Enter mark for {student.name}: ")) * 10)
                    / 10
                )
                student.marks[course_id] = mark

    def _input_interface(self):
        self._input_info()
        self._input_marks()
