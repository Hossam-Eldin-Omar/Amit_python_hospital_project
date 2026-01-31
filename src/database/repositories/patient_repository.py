from uuid import UUID, uuid4
from typing import List, Optional
from datetime import date
from src.database.connection import ScyllaDBConnection
from src.models.patient import Patient
import logging

logger = logging.getLogger(__name__)


class PatientRepository:
    """Data access layer for Patient operations.

    Patients are partitioned by department_id (FK → departments).
    """

    def __init__(self, session=None):
        self.db = ScyllaDBConnection() if session is None else None
        self.session = session or self.db.connect()
        self.session.set_keyspace("hospital")

    # ---------------------------------------------------------- #
    # CREATE
    # ---------------------------------------------------------- #
    def create(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        age: int,
        phone: str,
        department_id: UUID,
        medical_record: str = None,
    ) -> str:
        """Insert a new patient and return patient_id."""

        if not department_id:
            raise ValueError("department_id is required")

        patient_id = uuid4()

        insert_query = """
        INSERT INTO patients (
            department_id, patient_id, first_name, last_name,
            date_of_birth, age, phone, medical_record, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, toTimestamp(now()))
        """

        try:
            prepared = self.session.prepare(insert_query)
            self.session.execute(
                prepared,
                [
                    department_id,
                    patient_id,
                    first_name,
                    last_name,
                    date_of_birth,
                    age,
                    phone,
                    medical_record,
                ],
            )

            logger.info(
                f"Patient {first_name} {last_name} created with ID {patient_id}"
            )
            return str(patient_id)

        except Exception:
            logger.exception("Error creating patient")
            raise

    # ---------------------------------------------------------- #
    # READ – by ID
    # ---------------------------------------------------------- #
    def find_by_id(self, patient_id, department_id=None) -> Optional[Patient]:
        if isinstance(patient_id, str):
            patient_id = UUID(patient_id)

        if department_id and isinstance(department_id, str):
            department_id = UUID(department_id)

        if not department_id:
            return self._find_by_id_scan(patient_id)

        query = "SELECT * FROM patients WHERE department_id = ? AND patient_id = ?"
        prepared = self.session.prepare(query)
        row = self.session.execute(prepared, [department_id, patient_id]).one()
        return self._row_to_patient(row) if row else None

    def _find_by_id_scan(self, patient_id: UUID) -> Optional[Patient]:
        query = "SELECT * FROM patients WHERE patient_id = ? ALLOW FILTERING"
        prepared = self.session.prepare(query)
        row = self.session.execute(prepared, [patient_id]).one()
        return self._row_to_patient(row) if row else None

    # ---------------------------------------------------------- #
    # READ – by department
    # ---------------------------------------------------------- #
    def find_by_department(self, department_id: UUID) -> List[Patient]:
        if isinstance(department_id, str):
            department_id = UUID(department_id)

        query = "SELECT * FROM patients WHERE department_id = ?"
        prepared = self.session.prepare(query)
        results = self.session.execute(prepared, [department_id])
        return [self._row_to_patient(row) for row in results]

    # ---------------------------------------------------------- #
    # READ – by name
    # ---------------------------------------------------------- #
    def find_by_name(self, first_name: str = None, last_name: str = None) -> List[Patient]:
        if not first_name and not last_name:
            return []

        conditions = []
        params = []

        if first_name:
            conditions.append("first_name = ?")
            params.append(first_name)
        if last_name:
            conditions.append("last_name = ?")
            params.append(last_name)

        query = (
            "SELECT * FROM patients WHERE "
            + " AND ".join(conditions)
            + " ALLOW FILTERING"
        )

        prepared = self.session.prepare(query)
        results = self.session.execute(prepared, params)
        return [self._row_to_patient(row) for row in results]

    # ---------------------------------------------------------- #
    # UPDATE
    # ---------------------------------------------------------- #
    def update(self, department_id: UUID, patient_id: UUID, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        update_query = f"""
        UPDATE patients
        SET {set_clause}
        WHERE department_id = ? AND patient_id = ?
        """

        values = list(kwargs.values()) + [department_id, patient_id]

        prepared = self.session.prepare(update_query)
        self.session.execute(prepared, values)
        return True

    # ---------------------------------------------------------- #
    # DELETE
    # ---------------------------------------------------------- #
    def delete(self, department_id: UUID, patient_id: UUID) -> bool:
        query = "DELETE FROM patients WHERE department_id = ? AND patient_id = ?"
        prepared = self.session.prepare(query)
        self.session.execute(prepared, [department_id, patient_id])
        return True

    # ---------------------------------------------------------- #
    # READ – all
    # ---------------------------------------------------------- #
    def get_all(self) -> List[Patient]:
        results = self.session.execute("SELECT * FROM patients")
        return [self._row_to_patient(row) for row in results]

    # ---------------------------------------------------------- #
    # Helper
    # ---------------------------------------------------------- #
    @staticmethod
    def _row_to_patient(row) -> Patient:
        return Patient(
            first_name=row.first_name,
            last_name=row.last_name,
            age=row.age,
            date_of_birth=row.date_of_birth,
            phone=row.phone,
            patient_id=row.patient_id,
            department_id=row.department_id,
            medical_record=getattr(row, "medical_record", None),
            created_at=row.created_at,
        )
