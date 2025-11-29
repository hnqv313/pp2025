from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class StudentMarks:
    id: int = 0
    name: str = "Unknown"
    DoB: datetime = field(
        default_factory=lambda: datetime.strptime("1-1-1990", "%d-%m-%Y")
    )
    marks: Dict[int, float] = field(default_factory=dict)  # key: course_id, value: mark


@dataclass
class Courses:
    id: int = 0
    name: str = "Unknown"
    students: StudentMarks = field(default_factory=StudentMarks)


def input_student_info(student: StudentMarks):
    student.id = int(input("ID: "))
    student.name = input("Name: ")
    student.DoB = datetime.strptime(input("DoB (DD-MM-YYYY): "), "%d-%m-%Y")


def input_course_info(courses: Courses):
    courses.id = int(input("Course ID: "))
    courses.name = input("Course Name: ")


def input_info():
    students: Dict[int, StudentMarks] = {}
    student_number: int = int(input("Enter number of students: "))
    for _ in range(student_number):
        print()
        student = StudentMarks()
        input_student_info(student)
        students[student.id] = student

    print()
    courses: Dict[int, Courses] = {}
    course_number: int = int(input("Enter number of courses: "))
    for _ in range(course_number):
        print()
        course = Courses()
        input_course_info(courses=course)
        courses[course.id] = course

    return students, courses


def input_marks(students: Dict[int, StudentMarks], courses: Dict[int, Courses]):
    while True:
        print("\nAvailable courses:")
        for course in courses.values():
            print(f"{course.id}: {course.name}")

        course_id: str | int = input(
            "Select a course ID to input marks (Enter to cancel): "
        )

        if not course_id.isdigit() and course_id.strip() == "":
            print("Cancel mark input.")
            break

        course_id = int(course_id)

        if course_id not in courses:
            raise ValueError("Invalid course ID!")

        print(f"\nInput marks for course: {courses[course_id].name}")
        for student in students.values():
            mark = float(input(f"Enter mark for {student.name}: "))
            student.marks[course_id] = mark


def main():
    students, courses = input_info()
    input_marks(students=students, courses=courses)

    print("\nAll Students:")
    for student in students.values():
        marks_str: str = ", ".join(
            f"{courses[cid].name}: {mark}" for cid, mark in student.marks.items()
        )
        print(
            f"ID: {student.id}, Name: {student.name}, DoB: {
                student.DoB.strftime('%d-%m-%Y')
            }, Marks: {marks_str}"
        )


if __name__ == "__main__":
    main()
