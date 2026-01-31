from uuid import uuid4
from datetime import datetime


class Person:
    """Base Person class – parent of Patient and Staff (UML inheritance)."""

    def __init__(self, name: str, age: int, person_id=None):
        self.person_id = person_id or uuid4()
        self.name = name
        self.age = age
        self.created_at = datetime.now()

    def view_info(self) -> str:
        """Display person information."""
        return f"Name: {self.name}, Age: {self.age}"

    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "person_id": self.person_id,
            "name": self.name,
            "age": self.age,
            "created_at": self.created_at,
        }
