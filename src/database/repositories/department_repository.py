from uuid import UUID, uuid4
from typing import List, Optional
from src.database.connection import ScyllaDBConnection
from src.models.department import Department
import logging

logger = logging.getLogger(__name__)


class DepartmentRepository:
    """Data access layer for Department operations.

    Departments are partitioned by hospital_id (FK → hospitals).
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
        name: str,
        hospital_id: UUID,
        description: str = None,
        head_doctor_id: int = None,
    ) -> Optional[str]:
        """Insert a new department. Returns department_id or None."""
        department_id = uuid4()
        if isinstance(hospital_id, str):
            hospital_id = UUID(hospital_id)

        query = """
        INSERT INTO departments (
            hospital_id, department_id, name, description, head_doctor_id, created_at
        ) VALUES (?, ?, ?, ?, ?, toTimestamp(now()))
        """
        try:
            prepared = self.session.prepare(query)
            self.session.execute(
                prepared,
                [hospital_id, department_id, name, description, head_doctor_id],
            )
            logger.info(
                f"Department '{name}' created in hospital {hospital_id} "
                f"with ID {department_id}"
            )
            return str(department_id)
        except Exception as e:
            logger.error(f"Error creating department: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – by ID (requires hospital_id for partition key)
    # ---------------------------------------------------------- #
    def find_by_id(
        self, department_id, hospital_id=None
    ) -> Optional[Department]:
        """Find a department by its ID, optionally scoped to a hospital."""
        if isinstance(department_id, str):
            department_id = UUID(department_id)
        if hospital_id and isinstance(hospital_id, str):
            hospital_id = UUID(hospital_id)

        if not hospital_id:
            return self._find_by_id_scan(department_id)

        query = """
        SELECT * FROM departments
        WHERE hospital_id = ? AND department_id = ?
        """
        try:
            prepared = self.session.prepare(query)
            row = self.session.execute(prepared, [hospital_id, department_id]).one()
            return self._row_to_department(row) if row else None
        except Exception as e:
            logger.error(f"Error finding department: {e}")
            return None

    def _find_by_id_scan(self, department_id: UUID) -> Optional[Department]:
        """Scan all partitions for a department (use with caution)."""
        query = "SELECT * FROM departments WHERE department_id = ? ALLOW FILTERING"
        try:
            prepared = self.session.prepare(query)
            row = self.session.execute(prepared, [department_id]).one()
            return self._row_to_department(row) if row else None
        except Exception as e:
            logger.error(f"Error scanning for department: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – by hospital
    # ---------------------------------------------------------- #
    def find_by_hospital(self, hospital_id: UUID) -> List[Department]:
        """Find all departments belonging to a hospital."""
        if isinstance(hospital_id, str):
            hospital_id = UUID(hospital_id)

        query = "SELECT * FROM departments WHERE hospital_id = ?"
        try:
            prepared = self.session.prepare(query)
            results = self.session.execute(prepared, [hospital_id])
            departments = [self._row_to_department(row) for row in results]
            logger.info(
                f"Found {len(departments)} departments in hospital {hospital_id}"
            )
            return departments
        except Exception as e:
            logger.error(f"Error finding departments by hospital: {e}")
            return []

    # ---------------------------------------------------------- #
    # READ – all
    # ---------------------------------------------------------- #
    def get_all(self) -> List[Department]:
        """Get all departments across all hospitals."""
        query = "SELECT * FROM departments"
        try:
            results = self.session.execute(query)
            return [self._row_to_department(row) for row in results]
        except Exception as e:
            logger.error(f"Error getting all departments: {e}")
            return []

    # ---------------------------------------------------------- #
    # UPDATE
    # ---------------------------------------------------------- #
    def update(
        self, hospital_id: UUID, department_id: UUID, **kwargs
    ) -> bool:
        """Update department fields dynamically."""
        if not kwargs:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        query = f"""
        UPDATE departments SET {set_clause}
        WHERE hospital_id = ? AND department_id = ?
        """
        values = list(kwargs.values()) + [hospital_id, department_id]
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, values)
            logger.info(f"Department {department_id} updated")
            return True
        except Exception as e:
            logger.error(f"Error updating department: {e}")
            return False

    # ---------------------------------------------------------- #
    # DELETE
    # ---------------------------------------------------------- #
    def delete(self, hospital_id: UUID, department_id: UUID) -> bool:
        """Delete a department."""
        query = """
        DELETE FROM departments
        WHERE hospital_id = ? AND department_id = ?
        """
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, [hospital_id, department_id])
            logger.info(f"Department {department_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting department: {e}")
            return False

    # ---------------------------------------------------------- #
    # Helper
    # ---------------------------------------------------------- #
    @staticmethod
    def _row_to_department(row) -> Department:
        return Department(
            name=row.name,
            hospital_id=row.hospital_id,
            description=row.description,
            head_doctor_id=row.head_doctor_id,
            department_id=row.department_id,
            created_at=row.created_at,
        )
