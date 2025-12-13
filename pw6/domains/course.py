from dataclasses import dataclass


@dataclass
class Courses:
    id: str = "0"
    name: str = "Unknown"
    credits: int = 0
