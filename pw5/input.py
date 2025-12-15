import json
import math
import os
from dataclasses import asdict
from datetime import datetime
from functools import wraps
from typing import Dict

from domains.course import Courses
from domains.database import AutoSave, StudentMarksDatabase
from domains.student import StudentMarks


class Helper:
    @staticmethod
    def auto_save(file: str):
        AutoSave.files.append(os.path.abspath(file))
        with open(AutoSave.files[0], "w", encoding="utf-8") as f:
            for file in AutoSave.files:
                f.write(f"{file}\n")

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)

                with open(file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False, default=str)

                return result

            return wrapper

        return decorator


class StudentMarksInput(StudentMarksDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _input_student_info_helper(self, student: StudentMarks):
        student.id = input("ID: ")
        student.name = input("Name: ")
        student.DoB = datetime.strptime(input("DoB (DD-MM-YYYY): "), "%d-%m-%Y")

    def _input_course_info_helper(self, courses: Courses):
        courses.id = input("Course ID: ")
        courses.name = input("Course Name: ")
        courses.credits = int(input("Credits: "))

    @Helper.auto_save("students.txt")
    def _input_student_info(self) -> Dict:
        student_number: int = int(input("\nEnter number of students: "))
        for _ in range(student_number):
            print()
            student = StudentMarks()
            self._input_student_info_helper(student)
            self._students[student.id] = student

        return {
            sid: {
                **{k: v for k, v in asdict(student).items() if k != "marks"},
                "DoB": student.DoB.isoformat(),
            }
            for sid, student in self._students.items()
        }

    @Helper.auto_save("courses.txt")
    def _input_course_info(self) -> Dict:
        course_number: int = int(input("\nEnter number of courses: "))
        for _ in range(course_number):
            print()
            course = Courses()
            self._input_course_info_helper(courses=course)
            self._courses[course.id] = course

        return {k: asdict(v) for k, v in self._courses.items()}

    @Helper.auto_save("marks.txt")
    def _input_marks(self) -> Dict[str, Dict[str, float]]:
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

        return {sid: student.marks for sid, student in self._students.items()}

    def _input_interface(self):
        self._input_student_info()
        self._input_course_info()
        self._input_marks()
