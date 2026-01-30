from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime
from cassandra.query import SimpleStatement
from src.database.connection import ScyllaDBConnection
from src.models.patient import Patient
import logging

logger = logging.getLogger(__name__)


class PatientRepository:
    """Data access layer for Patient operations"""

    def __init__(self, session=None):
        """Initialize repository with optional session"""
        self.db = ScyllaDBConnection() if session is None else None
        self.session = session or self.db.connect()
        self.session.set_keyspace("hospital")

    def create(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        age: int,
        phone: str,
        department_id: UUID = None,
    ) -> str:
        """
        Insert a new patient into the database

        Args:
            first_name: Patient's first name
            last_name: Patient's last name
            date_of_birth: DOB in YYYY-MM-DD format
            age: Patient's age
            phone: Contact phone number
            department_id: Optional department UUID (auto-generated if not provided)

        Returns:
            str: patient_id of created patient, or None if failed
        """
        patient_id = uuid4()
        department_id = department_id or uuid4()

        insert_query = """
        INSERT INTO patients (
            department_id, patient_id, first_name, last_name, 
            date_of_birth, age, phone, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, toTimestamp(now()))
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
                ],
            )

            logger.info(
                f"Patient {first_name} {last_name} created successfully with ID {patient_id}"
            )
            return str(patient_id)

        except Exception as e:
            logger.error(f"Error creating patient: {e}")
            return None

    def find_by_id(self, patient_id, department_id=None) -> Optional[Patient]:
        """
        Find patient by ID

        Args:
            patient_id: UUID of patient (can be UUID object or string)
            department_id: Department UUID (can be UUID object, string, or None)

        Returns:
            Patient: Patient object or None
        """
        # Convert string UUIDs to UUID objects
        if isinstance(patient_id, str):
            try:
                patient_id = UUID(patient_id)
            except ValueError:
                logger.error(f"Invalid patient_id format: {patient_id}")
                return None

        if department_id and isinstance(department_id, str):
            try:
                department_id = UUID(department_id)
            except ValueError:
                logger.error(f"Invalid department_id format: {department_id}")
                return None

        if not department_id:
            logger.warning("Department ID not provided, scanning all partitions")
            return self._find_by_id_scan(patient_id)

        query = "SELECT * FROM patients WHERE department_id = ? AND patient_id = ?"

        try:
            prepared = self.session.prepare(query)
            result = self.session.execute(prepared, [department_id, patient_id])
            row = result.one()

            if row:
                return Patient(
                    first_name=row.first_name,
                    last_name=row.last_name,
                    age=row.age,
                    date_of_birth=row.date_of_birth,
                    phone=row.phone,
                    patient_id=row.patient_id,
                    department_id=row.department_id,
                    created_at=row.created_at,
                )
            return None

        except Exception as e:
            logger.error(f"Error finding patient: {e}")
            return None

    def _find_by_id_scan(self, patient_id: UUID) -> Optional[Patient]:
        """Scan all partitions for patient (inefficient, use with caution)"""
        query = "SELECT * FROM patients WHERE patient_id = ? ALLOW FILTERING"

        try:
            prepared = self.session.prepare(query)
            result = self.session.execute(prepared, [patient_id])
            row = result.one()

            if row:
                return Patient(
                    first_name=row.first_name,
                    last_name=row.last_name,
                    age=row.age,
                    date_of_birth=row.date_of_birth,
                    phone=row.phone,
                    patient_id=row.patient_id,
                    department_id=row.department_id,
                    created_at=row.created_at,
                )
            return None

        except Exception as e:
            logger.error(f"Error finding patient by scan: {e}")
            return None

    def find_by_department(self, department_id: UUID) -> List[Patient]:
        """
        Find all patients in a department

        Args:
            department_id: UUID of department

        Returns:
            List[Patient]: List of Patient objects
        """
        query = "SELECT * FROM patients WHERE department_id = ?"

        try:
            prepared = self.session.prepare(query)
            results = self.session.execute(prepared, [department_id])

            patients = []
            for row in results:
                patient = Patient(
                    first_name=row.first_name,
                    last_name=row.last_name,
                    age=row.age,
                    date_of_birth=row.date_of_birth,
                    phone=row.phone,
                    patient_id=row.patient_id,
                    department_id=row.department_id,
                    created_at=row.created_at,
                )
                patients.append(patient)

            logger.info(f"Found {len(patients)} patients in department {department_id}")
            return patients

        except Exception as e:
            logger.error(f"Error finding patients by department: {e}")
            return []

    def find_by_name(
        self, first_name: str = None, last_name: str = None
    ) -> List[Patient]:
        """
        Find patients by name (uses ALLOW FILTERING - inefficient)

        Args:
            first_name: Patient's first name (optional)
            last_name: Patient's last name (optional)

        Returns:
            List[Patient]: Matching Patient objects
        """
        if not first_name and not last_name:
            logger.error("At least one name parameter required")
            return []

        query = "SELECT * FROM patients WHERE "
        params = []

        if first_name:
            query += "first_name = ?"
            params.append(first_name)

        if first_name and last_name:
            query += " AND "

        if last_name:
            query += "last_name = ?"
            params.append(last_name)

        query += " ALLOW FILTERING"

        try:
            prepared = self.session.prepare(query)
            results = self.session.execute(prepared, params)

            patients = []
            for row in results:
                patient = Patient(
                    first_name=row.first_name,
                    last_name=row.last_name,
                    age=row.age,
                    date_of_birth=row.date_of_birth,
                    phone=row.phone,
                    patient_id=row.patient_id,
                    department_id=row.department_id,
                    created_at=row.created_at,
                )
                patients.append(patient)

            return patients

        except Exception as e:
            logger.error(f"Error finding patients by name: {e}")
            return []

    def update(self, department_id: UUID, patient_id: UUID, **kwargs) -> bool:
        """
        Update patient information

        Args:
            department_id: Department UUID
            patient_id: Patient UUID
            **kwargs: Fields to update (first_name, last_name, phone, age, etc.)

        Returns:
            bool: Success status
        """
        if not kwargs:
            logger.warning("No fields to update")
            return False

        # Build dynamic update query
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        update_query = f"""
        UPDATE patients 
        SET {set_clause}
        WHERE department_id = ? AND patient_id = ?
        """

        values = list(kwargs.values()) + [department_id, patient_id]

        try:
            prepared = self.session.prepare(update_query)
            self.session.execute(prepared, values)

            logger.info(f"Patient {patient_id} updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error updating patient: {e}")
            return False

    def delete(self, department_id: UUID, patient_id: UUID) -> bool:
        """
        Delete a patient

        Args:
            department_id: Department UUID
            patient_id: Patient UUID

        Returns:
            bool: Success status
        """
        delete_query = "DELETE FROM patients WHERE department_id = ? AND patient_id = ?"

        try:
            prepared = self.session.prepare(delete_query)
            self.session.execute(prepared, [department_id, patient_id])

            logger.info(f"Patient {patient_id} deleted successfully")
            return True

        except Exception as e:
            logger.error(f"Error deleting patient: {e}")
            return False

    def get_all(self) -> List[Patient]:
        """
        Get all patients (use with caution on large datasets)

        Returns:
            List[Patient]: All patients in database
        """
        query = "SELECT * FROM patients"

        try:
            results = self.session.execute(query)

            patients = []
            for row in results:
                patient = Patient(
                    first_name=row.first_name,
                    last_name=row.last_name,
                    age=row.age,
                    date_of_birth=row.date_of_birth,
                    phone=row.phone,
                    patient_id=row.patient_id,
                    department_id=row.department_id,
                    created_at=row.created_at,
                )
                patients.append(patient)

            logger.info(f"Retrieved {len(patients)} total patients")
            return patients

        except Exception as e:
            logger.error(f"Error getting all patients: {e}")
            return []
