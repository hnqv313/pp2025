from domains.database import StudentMarksDatabase


class StudentMarksOutput(StudentMarksDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

            if student_mark is None:
                raise ValueError("Course ID not found.")

            print(student.name, student_mark, sep=": ")

    def _list_students_by_gpa(self):
        students_with_gpa = [
            (student, self.calculate_gpa(student))
            for student in self._students.values()
        ]

        students_with_gpa.sort(key=lambda x: x[1], reverse=True)

        for student, gpa in students_with_gpa:
            print(f"{student.name} - GPA: {gpa:.2f}")


#
