from uuid import uuid4
from datetime import datetime


class Department:
    """Department class – belongs to a Hospital (1:*) and manages Patients & Staff."""

    def __init__(
        self,
        name: str,
        hospital_id,
        description: str = None,
        head_doctor_id=None,
        department_id=None,
        created_at=None,
    ):
        self.department_id = department_id or uuid4()
        self.hospital_id = hospital_id          # FK → Hospital (UML "contains")
        self.name = name
        self.description = description
        self.head_doctor_id = head_doctor_id
        self.created_at = created_at or datetime.now()

        # In-memory caches populated by the repository layer
        self.patients = []       # Department "manages" many Patients
        self.staff_members = []  # Department "employs" many Staff

    # ------------------------------------------------------------------ #
    # UML: add_patient(patient: Patient): void
    # ------------------------------------------------------------------ #
    def add_patient(self, patient) -> None:
        """Add a patient to this department (in-memory list)."""
        self.patients.append(patient)

    # ------------------------------------------------------------------ #
    # UML: add_staff(staff_member: Staff): void
    # ------------------------------------------------------------------ #
    def add_staff(self, staff_member) -> None:
        """Add a staff member to this department (in-memory list)."""
        self.staff_members.append(staff_member)

    def view_info(self) -> str:
        """Display department information."""
        return (
            f"Department: {self.name} (ID: {self.department_id}), "
            f"Hospital: {self.hospital_id}, "
            f"Description: {self.description}"
        )

    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "hospital_id": self.hospital_id,
            "department_id": self.department_id,
            "name": self.name,
            "description": self.description,
            "head_doctor_id": self.head_doctor_id,
            "created_at": self.created_at,
        }
