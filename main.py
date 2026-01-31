"""Main entry point for the hospital management system.

Demonstrates the full UML relationship chain:
    Hospital  --contains-->  Department  --manages-->  Patient
                                          --employs-->  Staff
"""
import sys
from datetime import datetime
from uuid import uuid4, UUID

from src.database.connection import ScyllaDBConnection
from src.database.init_db import initialize_database
from src.database.repositories.hospital_repository import HospitalRepository
from src.database.repositories.department_repository import DepartmentRepository
from src.database.repositories.patient_repository import PatientRepository
from src.database.repositories.staff_repository import StaffRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


# ------------------------------------------------------------------ #
# Input helpers
# ------------------------------------------------------------------ #
def get_hospital_input():
    name = input("Hospital name: ").strip()
    location = input("Location: ").strip()
    phone = input("Phone (optional): ").strip() or None
    if not name or not location:
        raise ValueError("Name and location are required")
    return name, location, phone


def get_department_input(hospitals):
    """Pick an existing hospital, then enter department details."""
    if not hospitals:
        raise ValueError("No hospitals exist yet. Create one first.")

    print("\nAvailable hospitals:")
    for i, h in enumerate(hospitals):
        print(f"  [{i}] {h.name} – {h.location} (ID: {h.hospital_id})")

    idx = int(input("Select hospital index: "))
    hospital = hospitals[idx]

    name = input("Department name: ").strip()
    description = input("Description (optional): ").strip() or None
    if not name:
        raise ValueError("Department name is required")
    return hospital.hospital_id, name, description


def get_patient_input(departments):
    """Pick an existing department, then enter patient details."""
    if not departments:
        raise ValueError("No departments exist yet. Create one first.")

    print("\nAvailable departments:")
    for i, d in enumerate(departments):
        print(f"  [{i}] {d.name} – Hospital: {d.hospital_id} (Dept ID: {d.department_id})")

    idx = int(input("Select department index: "))
    department = departments[idx]

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    phone = input("Phone: ").strip()
    medical_record = input("Medical record note (optional): ").strip() or None

    age = int((datetime.now() - datetime.strptime(dob, "%Y-%m-%d")).days / 365.25)
    datetime.strptime(dob, "%Y-%m-%d")  # validate

    if not first_name or not last_name:
        raise ValueError("First and last name are required")
    return department.department_id, first_name, last_name, dob, age, phone, medical_record


def get_staff_input(departments):
    """Pick an existing department, then enter staff details."""
    if not departments:
        raise ValueError("No departments exist yet. Create one first.")

    print("\nAvailable departments:")
    for i, d in enumerate(departments):
        print(f"  [{i}] {d.name} – Hospital: {d.hospital_id} (Dept ID: {d.department_id})")

    idx = int(input("Select department index: "))
    department = departments[idx]

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    age = int(input("Age: ").strip())
    position = input("Position (e.g. Doctor, Nurse): ").strip()

    if not first_name or not last_name or not position:
        raise ValueError("First name, last name, and position are required")
    return department.department_id, first_name, last_name, age, position


# ------------------------------------------------------------------ #
# Display helpers
# ------------------------------------------------------------------ #
def display_all(hosp_repo, dept_repo, patient_repo, staff_repo):
    """Print a full tree: Hospital → Departments → Patients & Staff."""
    hospitals = hosp_repo.get_all()
    if not hospitals:
        logger.info("No hospitals in the system.")
        return hospitals, []

    all_departments = []
    for hospital in hospitals:
        logger.info(f"\n🏥  {hospital.name} | {hospital.location} | {hospital.phone}")
        logger.info(f"    Hospital ID: {hospital.hospital_id}")

        departments = dept_repo.find_by_hospital(hospital.hospital_id)
        all_departments.extend(departments)

        if not departments:
            logger.info("    └─ (no departments)")
            continue

        for dept in departments:
            logger.info(f"    🏢  {dept.name} – {dept.description or 'no description'}")
            logger.info(f"        Department ID: {dept.department_id}")

            # Patients managed by this department
            patients = patient_repo.find_by_department(dept.department_id)
            if patients:
                logger.info("        👥 Patients:")
                for p in patients:
                    logger.info(
                        f"            • {p.first_name} {p.last_name} | "
                        f"Age: {p.age} | Phone: {p.phone} | "
                        f"Medical Record: {p.medical_record or 'N/A'}"
                    )
            else:
                logger.info("        👥 Patients: (none)")

            # Staff employed by this department
            staff = staff_repo.find_by_department(dept.department_id)
            if staff:
                logger.info("        👔 Staff:")
                for s in staff:
                    logger.info(
                        f"            • {s.first_name} {s.last_name} | "
                        f"Position: {s.position} | Age: {s.age}"
                    )
            else:
                logger.info("        👔 Staff: (none)")

    return hospitals, all_departments


# ------------------------------------------------------------------ #
# Main menu
# ------------------------------------------------------------------ #
def main():
    logger.info("=" * 60)
    logger.info("Hospital Management System")
    logger.info("=" * 60)

    try:
        db = ScyllaDBConnection()
        session = db.connect()
        initialize_database(session)

        hosp_repo = HospitalRepository(session=session)
        dept_repo = DepartmentRepository(session=session)
        patient_repo = PatientRepository(session=session)
        staff_repo = StaffRepository(session=session)

        while True:
            logger.info("\n--- Menu ---")
            logger.info("1. Add Hospital")
            logger.info("2. Add Department")
            logger.info("3. Add Patient")
            logger.info("4. Add Staff")
            logger.info("5. View all (tree)")
            logger.info("6. Exit")

            choice = input("Choice (1-6): ").strip()

            if choice == "1":
                try:
                    name, location, phone = get_hospital_input()
                    hid = hosp_repo.create(name, location, phone)
                    logger.info(f"✓ Hospital created: {hid}")
                except ValueError as ve:
                    logger.error(f"Input error: {ve}")

            elif choice == "2":
                hospitals, _ = display_all(hosp_repo, dept_repo, patient_repo, staff_repo)
                try:
                    hospital_id, name, description = get_department_input(hospitals)
                    did = dept_repo.create(name, hospital_id, description)
                    logger.info(f"✓ Department created: {did}")
                except (ValueError, IndexError) as e:
                    logger.error(f"Input error: {e}")

            elif choice == "3":
                _, departments = display_all(hosp_repo, dept_repo, patient_repo, staff_repo)
                try:
                    dept_id, fn, ln, dob, age, phone, med = get_patient_input(departments)
                    pid = patient_repo.create(fn, ln, dob, age, phone, dept_id, med)
                    logger.info(f"✓ Patient created: {pid}")
                except (ValueError, IndexError) as e:
                    logger.error(f"Input error: {e}")

            elif choice == "4":
                _, departments = display_all(hosp_repo, dept_repo, patient_repo, staff_repo)
                try:
                    dept_id, fn, ln, age, position = get_staff_input(departments)
                    sid = staff_repo.create(fn, ln, age, position, dept_id)
                    logger.info(f"✓ Staff created: {sid}")
                except (ValueError, IndexError) as e:
                    logger.error(f"Input error: {e}")

            elif choice == "5":
                display_all(hosp_repo, dept_repo, patient_repo, staff_repo)

            elif choice == "6":
                logger.info("Goodbye!")
                break
            else:
                logger.warning("Invalid choice.")

        db.close()

    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
