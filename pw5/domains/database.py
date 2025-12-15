import json
from datetime import datetime
from typing import Dict, List

import numpy

from domains.course import Courses
from domains.student import StudentMarks


class AutoSave:
    files: List[str] = [".auto_save"]

    @staticmethod
    def list_paths() -> List[str]:
        with open(AutoSave.files[0], "r", encoding="utf-8") as f:
            next(f, None)
            file_paths = [line.strip() for line in f if line.strip()]
        return list(dict.fromkeys(file_paths))


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

    def load_students(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sid, info in data.items():
                info["DoB"] = datetime.fromisoformat(info["DoB"])
                self._students[sid] = StudentMarks(**info)

    def load_courses(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for cid, info in data.items():
                self._courses[cid] = Courses(**info)

    def load_marks(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sid, marks in data.items():
                if sid in self._students:
                    self._students[sid].marks.update(marks)
