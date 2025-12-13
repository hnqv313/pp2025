import gzip
import io
import json
import os
import pickle
from dataclasses import asdict
from datetime import datetime
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

    def export_to_json(self, filename: str = "students.dat"):
        data = {
            "courses": [asdict(c) for c in self._courses.values()],
            "students": [asdict(s) for s in self._students.values()],
        }

        try:
            with gzip.open(filename, "wb") as f:
                with io.TextIOWrapper(f, encoding="utf-8") as wrapper:
                    json.dump(data, wrapper, indent=4, ensure_ascii=False, default=str)
            print(f"Exported to {filename}")
        except Exception as e:
            print(f"Export Error: {e}")

    def import_from_json(self, filename: str = "students.dat"):
        if not os.path.exists(filename):
            print("File not found.")
            return

        try:
            with gzip.open(filename, "rb") as f:
                with io.TextIOWrapper(f, encoding="utf-8") as wrapper:
                    data = json.load(wrapper)

            self._courses = {c["id"]: Courses(**c) for c in data.get("courses", [])}

            self._students = {}
            for s_data in data.get("students", []):
                if isinstance(s_data["DoB"], str):
                    try:
                        s_data["DoB"] = datetime.fromisoformat(s_data["DoB"])
                    except ValueError:
                        s_data["DoB"] = datetime.strptime(
                            s_data["DoB"], "%Y-%m-%d %H:%M:%S"
                        )

                student = StudentMarks(**s_data)
                self._students[student.id] = student

            print(f"Loaded from {filename}")

        except Exception as e:
            print(f"Import Error: {e}")

    def export_to_pickle(self, filename: str = "students.pkl.dat"):
        try:
            with gzip.open(filename, "wb") as f:
                pickle.dump((self._students, self._courses), f)
            print(f"Exported to {filename} (Pickle)")
        except Exception as e:
            print(f"Pickle Export Error: {e}")

    def import_from_pickle(self, filename: str = "students.pkl.dat"):
        input(
            "WARNING: Pickle is bad. It has security issues "
            "as it can execute malicious code during data import "
            "if proper validation is not performed.\n"
        )

        if not os.path.exists(filename):
            print("Pickle file not found.")
            return

        try:
            with gzip.open(filename, "rb") as f:
                self._students, self._courses = pickle.load(f)
            print(f"Loaded from {filename} (Pickle)")
        except Exception as e:
            print(f"Pickle Import Error: {e}")
