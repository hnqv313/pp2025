from typing import Dict, List

import numpy
from domains.course import Courses
from domains.student import StudentMarks


class StudentMarksDatabase:
    def __init__(self):
        self._students: Dict[str, StudentMarks] = {}
        self._courses: Dict[str, Courses] = {}

    def calculate_gpa(self, student: StudentMarks) -> float:
        marks: List[float] = []
        credits: List[int] = []

        for course_id, mark in student.marks.items():
            course = self._courses.get(course_id)
            if course:
                marks.append(mark)
                credits.append(course.credits)

        if not marks:
            return 0.0

        marks_arr = numpy.array(marks)
        credits_arr = numpy.array(credits)

        return numpy.sum(marks_arr * credits_arr) / numpy.sum(credits_arr)
