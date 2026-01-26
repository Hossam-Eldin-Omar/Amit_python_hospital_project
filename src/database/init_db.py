"""Database initialization module - creates keyspace and tables"""
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def initialize_database(session):
    """
    Initialize the hospital database schema.

    Args:
        session: Active Cassandra session
    """
    logger.debug("Initializing hospital database...")

    # Create keyspace
    create_keyspace(session)

    # Set keyspace
    session.set_keyspace("hospital")
    logger.debug("Using keyspace: hospital")

    # Create tables
    create_tables(session)

    logger.debug("✓ Database initialization complete")


def create_keyspace(session):
    """Create the hospital keyspace if it doesn't exist"""
    logger.debug("Creating hospital keyspace...")

    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS hospital
        WITH replication = {
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }
    """
    )

    logger.debug("✓ Keyspace 'hospital' created")


def create_tables(session):
    """Create all database tables"""
    # Hospitals table
    logger.debug("Creating hospitals table...")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS hospitals (
            hospital_id UUID PRIMARY KEY,
            name text,
            location text,
            phone text,
            created_at timestamp
        )
    """
    )
    logger.debug("✓ Hospitals table created")

    # Departments table
    logger.debug("Creating departments table...")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS departments (
            hospital_id UUID,        
            department_id UUID,
            name text,
            description text,
            head_doctor_id int,
            created_at timestamp,
            PRIMARY KEY (hospital_id, department_id)
        )
    """
    )
    logger.debug("✓ Departments table created")

    # Patients table
    logger.debug("Creating patients table...")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            department_id UUID,
            patient_id UUID,
            first_name text,
            last_name text,
            date_of_birth date,
            age int,
            phone text,
            created_at timestamp,
            PRIMARY KEY (department_id, patient_id)
        )

    """
    )
    logger.debug("✓ Patients table created")

    # Staff table
    logger.debug("Creating staff table...")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS staff (
            department_id UUID,
            staff_id UUID,
            name text,
            age int,
            position text,
            created_at timestamp,
            PRIMARY KEY (department_id, staff_id)
        )
    """
    )
    logger.debug("✓ Staff table created")


if __name__ == "__main__":
    """Run database initialization standalone"""
    from src.database.connection import ScyllaDBConnection

    logger.debug("=" * 60)
    logger.debug("Standalone Database Initialization")
    logger.debug("=" * 60)

    try:
        # Connect to database
        db = ScyllaDBConnection()
        session = db.connect()

        # Initialize database
        initialize_database(session)

        logger.debug("=" * 60)
        logger.debug("✅ Database initialization completed successfully!")
        logger.debug("=" * 60)

        # Close connection
        db.close()

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
