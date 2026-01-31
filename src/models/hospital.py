from uuid import uuid4
from datetime import datetime


class Hospital:
    """Hospital class – top-level container that owns departments."""

    def __init__(
        self,
        name: str,
        location: str,
        phone: str = None,
        hospital_id=None,
        created_at=None,
    ):
        self.hospital_id = hospital_id or uuid4()
        self.name = name
        self.location = location
        self.phone = phone
        self.created_at = created_at or datetime.now()
        self.departments = []  # in-memory cache of Department objects

    # ------------------------------------------------------------------ #
    # UML: add_department(department: Department): void
    # ------------------------------------------------------------------ #
    def add_department(self, department) -> None:
        """Add a department to this hospital (in-memory list)."""
        self.departments.append(department)

    def view_info(self) -> str:
        """Display hospital information."""
        return (
            f"Hospital: {self.name}, "
            f"Location: {self.location}, "
            f"Phone: {self.phone}"
        )

    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "hospital_id": self.hospital_id,
            "name": self.name,
            "location": self.location,
            "phone": self.phone,
            "created_at": self.created_at,
        }
