from uuid import UUID, uuid4
from typing import List, Optional
from src.database.connection import ScyllaDBConnection
from src.models.hospital import Hospital
import logging

logger = logging.getLogger(__name__)


class HospitalRepository:
    """Data access layer for Hospital operations."""

    def __init__(self, session=None):
        self.db = ScyllaDBConnection() if session is None else None
        self.session = session or self.db.connect()
        self.session.set_keyspace("hospital")

    # ---------------------------------------------------------- #
    # CREATE
    # ---------------------------------------------------------- #
    def create(self, name: str, location: str, phone: str = None) -> Optional[str]:
        """Insert a new hospital. Returns hospital_id or None."""
        hospital_id = uuid4()
        query = """
        INSERT INTO hospitals (hospital_id, name, location, phone, created_at)
        VALUES (?, ?, ?, ?, toTimestamp(now()))
        """
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, [hospital_id, name, location, phone])
            logger.info(f"Hospital '{name}' created with ID {hospital_id}")
            return str(hospital_id)
        except Exception as e:
            logger.error(f"Error creating hospital: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – by ID
    # ---------------------------------------------------------- #
    def find_by_id(self, hospital_id) -> Optional[Hospital]:
        """Find a hospital by its UUID."""
        if isinstance(hospital_id, str):
            try:
                hospital_id = UUID(hospital_id)
            except ValueError:
                logger.error(f"Invalid hospital_id: {hospital_id}")
                return None

        query = "SELECT * FROM hospitals WHERE hospital_id = ?"
        try:
            prepared = self.session.prepare(query)
            row = self.session.execute(prepared, [hospital_id]).one()
            return self._row_to_hospital(row) if row else None
        except Exception as e:
            logger.error(f"Error finding hospital: {e}")
            return None

    # ---------------------------------------------------------- #
    # READ – all
    # ---------------------------------------------------------- #
    def get_all(self) -> List[Hospital]:
        """Get all hospitals."""
        query = "SELECT * FROM hospitals"
        try:
            results = self.session.execute(query)
            return [self._row_to_hospital(row) for row in results]
        except Exception as e:
            logger.error(f"Error getting all hospitals: {e}")
            return []

    # ---------------------------------------------------------- #
    # UPDATE
    # ---------------------------------------------------------- #
    def update(self, hospital_id: UUID, **kwargs) -> bool:
        """Update hospital fields dynamically."""
        if not kwargs:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        query = f"UPDATE hospitals SET {set_clause} WHERE hospital_id = ?"
        values = list(kwargs.values()) + [hospital_id]
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, values)
            logger.info(f"Hospital {hospital_id} updated")
            return True
        except Exception as e:
            logger.error(f"Error updating hospital: {e}")
            return False

    # ---------------------------------------------------------- #
    # DELETE
    # ---------------------------------------------------------- #
    def delete(self, hospital_id: UUID) -> bool:
        """Delete a hospital."""
        query = "DELETE FROM hospitals WHERE hospital_id = ?"
        try:
            prepared = self.session.prepare(query)
            self.session.execute(prepared, [hospital_id])
            logger.info(f"Hospital {hospital_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting hospital: {e}")
            return False

    # ---------------------------------------------------------- #
    # Helper
    # ---------------------------------------------------------- #
    @staticmethod
    def _row_to_hospital(row) -> Hospital:
        return Hospital(
            name=row.name,
            location=row.location,
            phone=row.phone,
            hospital_id=row.hospital_id,
            created_at=row.created_at,
        )
