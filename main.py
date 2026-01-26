"""Main entry point for the hospital management system"""
import sys
from datetime import datetime
from uuid import uuid4

# Import from your src directory
from src.database.connection import ScyllaDBConnection
from src.database.init_db import initialize_database
from src.database.repositories.patient_repository import PatientRepository
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


def get_patient_input():
    """Read patient data from terminal input"""

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    age = int((datetime.now() - datetime.strptime(dob, "%Y-%m-%d")).days / 365.25)
    phone = input("Phone: ").strip()

    if not first_name or not last_name:
        raise ValueError("First name and last name are required")

    # Validate date format
    datetime.strptime(dob, "%Y-%m-%d")

    return first_name, last_name, dob, age, phone


def insert_patient(patient_repo, first_name, last_name, dob, age, phone):
    """Insert patient using PatientRepository"""
    try:
        patient_id = patient_repo.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=dob,
            age=age,
            phone=phone
        )
        
        if patient_id:
            logger.info(f"✓ Patient inserted with ID {patient_id}")
            return patient_id
        else:
            logger.error("Failed to insert patient")
            return None
            
    except Exception as e:
        logger.error(f"Error inserting patient: {e}")
        return None


def display_data(patient_repo):
    """Query and display data using PatientRepository"""
    try:
        logger.info("")
        logger.info("=" * 60)
        logger.info("PATIENTS IN DATABASE")
        logger.info("=" * 60)

        patients = patient_repo.get_all()
        
        if not patients:
            logger.info("No patients found in database")
        else:
            for patient in patients:
                logger.info(f"ID: {patient.patient_id} | {patient.first_name} {patient.last_name}")
                logger.info(f"  DOB: {patient.date_of_birth}")
                logger.info(f"  Age: {patient.age}")
                logger.info(f"  Phone: {patient.phone}")
                logger.info(f"  Department: {patient.department_id}")
                logger.info(f"  Created: {patient.created_at}")
                logger.info("")
                
    except Exception as e:
        logger.error(f"Error displaying patients: {e}")


def test_repository_operations(patient_repo):
    """Test various PatientRepository operations"""
    
    logger.info("=" * 60)
    logger.info("TESTING PATIENT REPOSITORY OPERATIONS")
    logger.info("=" * 60)
    
    # Test 1: Display all patients
    logger.info("\n[TEST 1] Get all patients:")
    display_data(patient_repo)
    
    # Test 2: Search patient by ID
    logger.info("[TEST 2] Search patient by ID:")
    patient_id_to_search = input("Enter patient ID to search (or press Enter to skip): ").strip()
    
    if patient_id_to_search:
        logger.info(f"Searching for patient ID: {patient_id_to_search}")
        patient = patient_repo.find_by_id(patient_id_to_search)
        
        if patient:
            logger.info("Patient found:")
            logger.info(f"  {patient.view_record()}")
            logger.info(f"  Contact: {patient.get_contact_info()}")
        else:
            logger.info("Patient not found")
    
    # Test 3: Search by name
    logger.info("\n[TEST 3] Search patients by name:")
    first_name = input("Enter first name to search (or press Enter to skip): ").strip()
    last_name = input("Enter last name to search (or press Enter to skip): ").strip()
    
    if first_name or last_name:
        patients = patient_repo.find_by_name(first_name=first_name if first_name else None,
                                            last_name=last_name if last_name else None)
        
        if patients:
            logger.info(f"Found {len(patients)} patient(s):")
            for patient in patients:
                logger.info(f"  - {patient.view_record()}")
        else:
            logger.info("No patients found with that name")
    
    logger.info("\n" + "=" * 60)


def main():
    """Main application entry point"""

    logger.info("=" * 60)
    logger.info("Hospital Management System - Starting")
    logger.info("=" * 60)

    try:
        # Connect to database
        db = ScyllaDBConnection()
        session = db.connect()

        # Initialize database schema
        logger.info("Initializing database schema...")
        initialize_database(session)

        # Initialize PatientRepository
        patient_repo = PatientRepository(session=session)

        # Menu for testing
        logger.info("\nSelect an option:")
        logger.info("1. Add new patient")
        logger.info("2. Test repository operations")
        logger.info("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Read patient data from user
            logger.info("Enter new patient data")
            try:
                patient_data = get_patient_input()
                insert_patient(patient_repo, *patient_data)
            except ValueError as ve:
                logger.error(f"Input error: {ve}")
            
            # Display all patients
            display_data(patient_repo)
            
        elif choice == "2":
            # Test repository operations
            test_repository_operations(patient_repo)
            
        logger.info("=" * 60)
        logger.info("✅ Application completed successfully!")
        logger.info("=" * 60)

        db.close()

    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
