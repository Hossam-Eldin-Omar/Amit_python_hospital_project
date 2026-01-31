from uuid import uuid4
from datetime import datetime
from src.models.person import Person


class Staff(Person):
    """Staff class extending Person – employed by a Department (UML "employs")."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int,
        position: str,
        staff_id=None,
        department_id=None,
        created_at=None,
    ):
        full_name = f"{first_name} {last_name}"
        super().__init__(name=full_name, age=age)

        self.staff_id = staff_id or uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.position = position              # UML attribute
        self.department_id = department_id    # FK → Department
        self.created_at = created_at or datetime.now()

    # ------------------------------------------------------------------ #
    # UML: view_info(): String
    # ------------------------------------------------------------------ #
    def view_info(self) -> str:
        """Display staff member's information."""
        return (
            f"Staff: {self.first_name} {self.last_name} "
            f"(ID: {self.staff_id}), "
            f"Position: {self.position}, Age: {self.age}, "
            f"Department: {self.department_id}"
        )

    def get_contact_info(self) -> str:
        """Get staff member contact information."""
        return f"{self.first_name} {self.last_name} - {self.position}"

    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "staff_id": self.staff_id,
            "department_id": self.department_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name": self.name,
            "age": self.age,
            "position": self.position,
            "created_at": self.created_at,
        }
