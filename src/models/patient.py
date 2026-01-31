from uuid import uuid4
from datetime import datetime
from src.models.person import Person


class Patient(Person):
    """Patient class extending Person – managed by a Department (UML "manages")."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int,
        date_of_birth: str,
        phone: str,
        patient_id=None,
        department_id=None,
        medical_record: str = None,
        created_at=None,
    ):
        full_name = f"{first_name} {last_name}"
        super().__init__(name=full_name, age=age)

        self.patient_id = patient_id or uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.department_id = department_id   # FK → Department
        self.medical_record = medical_record  # UML attribute
        self.created_at = created_at or datetime.now()

    # ------------------------------------------------------------------ #
    # UML: view_record(): String
    # ------------------------------------------------------------------ #
    def view_record(self) -> str:
        """Display patient's full record."""
        return (
            f"Patient: {self.first_name} {self.last_name} "
            f"(ID: {self.patient_id}), "
            f"DOB: {self.date_of_birth}, Age: {self.age}, "
            f"Phone: {self.phone}, "
            f"Department: {self.department_id}, "
            f"Medical Record: {self.medical_record or 'N/A'}"
        )

    def get_contact_info(self) -> str:
        """Get patient contact information."""
        return f"{self.first_name} {self.last_name}: {self.phone}"

    def to_dict(self):
        """Convert to dictionary for database storage."""
        return {
            "patient_id": self.patient_id,
            "department_id": self.department_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "age": self.age,
            "phone": self.phone,
            "medical_record": self.medical_record,
            "created_at": self.created_at,
        }
