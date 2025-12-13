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
