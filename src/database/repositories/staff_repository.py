from uuid import UUID, uuid4
from typing import List, Optional
from src.database.connection import ScyllaDBConnection
from src.models.staff import Staff
import logging

logger = logging.getLogger(__name__)


class StaffRepository:
    """Data access layer for Staff operations.

    Staff members are partitioned by department_id (FK → departments).
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
        age: int,
        position: str,
        department_id: UUID = None,
    ) -> Optional[str]:
        """
        Insert a new staff member.

        Args:
            first_name:    Staff's first name
            last_name:     Staff's last name
            age:           Staff's age
            position:      Job position / role
            department_id: Department UUID (auto-generated if not provided)

        Returns:
            str: staff_id or None on failure
        """
        staff_id = uuid4()
        department_id = department_id or uuid4()
        if isinstance(department_id, str):
            department_id = UUID(department_id)

        full_name = f"{first_name} {last_name}"

        query = """
        INSERT INTO staff (
            department_id, staff_id, first_name, last_name, name, age, position, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, toTimestamp(now()))
        """
        try:
            prepared = self.session.prepare(query)
            self.session.execute(
                prepared,
                [department_id, staff_id, first_name, last_name, full_name, age, position],
            )
            logger.info(
                f"Staff '{full_name}' created in department {department_id} "
                f"with ID {staff_id}"
            )
            return str(staff_id)
        except Exception as e:
            logger.error(f"Error creating staff: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – by ID
    # ---------------------------------------------------------- #
    def find_by_id(self, staff_id, department_id=None) -> Optional[Staff]:
        """Find a staff member by ID."""
        if isinstance(staff_id, str):
            try:
                staff_id = UUID(staff_id)
            except ValueError:
                logger.error(f"Invalid staff_id: {staff_id}")
                return None
        if department_id and isinstance(department_id, str):
            department_id = UUID(department_id)

        if not department_id:
            return self._find_by_id_scan(staff_id)

        query = "SELECT * FROM staff WHERE department_id = ? AND staff_id = ?"
        try:
            prepared = self.session.prepare(query)
            row = self.session.execute(prepared, [department_id, staff_id]).one()
            return self._row_to_staff(row) if row else None
        except Exception as e:
            logger.error(f"Error finding staff: {e}")
            return None

    def _find_by_id_scan(self, staff_id: UUID) -> Optional[Staff]:
        """Scan all partitions for a staff member."""
        query = "SELECT * FROM staff WHERE staff_id = ? ALLOW FILTERING"
        try:
            prepared = self.session.prepare(query)
            row = self.session.execute(prepared, [staff_id]).one()
            return self._row_to_staff(row) if row else None
        except Exception as e:
            logger.error(f"Error scanning for staff: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – by department
    # ---------------------------------------------------------- #
    def find_by_department(self, department_id: UUID) -> List[Staff]:
        """Find all staff members in a department."""
        if isinstance(department_id, str):
            department_id = UUID(department_id)

        query = "SELECT * FROM staff WHERE department_id = ?"
        try:
            prepared = self.session.prepare(query)
            results = self.session.execute(prepared, [department_id])
            staff_list = [self._row_to_staff(row) for row in results]
            logger.info(
                f"Found {len(staff_list)} staff in department {department_id}"
            )
            return staff_list
        except Exception as e:
            logger.error(f"Error finding staff by department: {e}")
            return []

    # ---------------------------------------------------------- #
    # READ – by name
    # ---------------------------------------------------------- #
    def find_by_name(
        self, first_name: str = None, last_name: str = None
    ) -> List[Staff]:
        """Find staff by name (uses ALLOW FILTERING)."""
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
            "SELECT * FROM staff WHERE "
            + " AND ".join(conditions)
            + " ALLOW FILTERING"
        )
        try:
            prepared = self.session.prepare(query)
            results = self.session.execute(prepared, params)
            return [self._row_to_staff(row) for row in results]
        except Exception as e:
            logger.error(f"Error finding staff by name: {e}")
            return []

    # ---------------------------------------------------------- #
    # READ – all
    # ---------------------------------------------------------- #
    def get_all(self) -> List[Staff]:
        """Get all staff members."""
        query = "SELECT * FROM staff"
        try:
            results = self.session.execute(query)
            return [self._row_to_staff(row) for row in results]
        except Exception as e:
            logger.error(f"Error getting all staff: {e}")
            return []

    # ---------------------------------------------------------- #
    # UPDATE
    # ---------------------------------------------------------- #
    def update(self, department_id: UUID, staff_id: UUID, **kwargs) -> bool:
        """Update staff fields dynamically."""
        if not kwargs:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        query = f"""
        UPDATE staff SET {set_clause}
        WHERE department_id = ? AND staff_id = ?
        """
        values = list(kwargs.values()) + [department_id, staff_id]
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, values)
            logger.info(f"Staff {staff_id} updated")
            return True
        except Exception as e:
            logger.error(f"Error updating staff: {e}")
            return False

    # ---------------------------------------------------------- #
    # DELETE
    # ---------------------------------------------------------- #
    def delete(self, department_id: UUID, staff_id: UUID) -> bool:
        """Delete a staff member."""
        query = "DELETE FROM staff WHERE department_id = ? AND staff_id = ?"
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, [department_id, staff_id])
            logger.info(f"Staff {staff_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting staff: {e}")
            return False

    # ---------------------------------------------------------- #
    # Helper
    # ---------------------------------------------------------- #
    @staticmethod
    def _row_to_staff(row) -> Staff:
        return Staff(
            first_name=row.first_name,
            last_name=row.last_name,
            age=row.age,
            position=row.position,
            staff_id=row.staff_id,
            department_id=row.department_id,
            created_at=row.created_at,
        )
