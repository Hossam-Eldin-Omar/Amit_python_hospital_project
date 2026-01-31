"""
Add Patient page – register a new patient linked to a specific department.

Flow: select Hospital → select Department → fill patient form → submit
"""

import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.hospital_repository import HospitalRepository
from src.database.repositories.department_repository import DepartmentRepository
from src.database.repositories.patient_repository import PatientRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@st.cache_resource
def get_repos():
    from src.database.connection import ScyllaDBConnection
    from src.database.init_db import initialize_database

    db = ScyllaDBConnection()
    session = db.connect()
    initialize_database(session)

    return (
        HospitalRepository(session=session),
        DepartmentRepository(session=session),
        PatientRepository(session=session),
    )


def calculate_age(dob):
    today = datetime.now().date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def render():
    st.markdown("# 👤 Add New Patient")
    st.markdown("Register a new patient linked to a hospital department")
    st.markdown("---")

    hosp_repo, dept_repo, patient_repo = get_repos()

    hospitals = hosp_repo.get_all() or []
    if not hospitals:
        st.warning("No hospitals exist.")
        return

    hospital_map = {h.name: h for h in hospitals}
    selected_hospital = hospital_map[
        st.selectbox("🏥 Select Hospital", hospital_map.keys())
    ]

    departments = dept_repo.find_by_hospital(selected_hospital.hospital_id) or []
    if not departments:
        st.warning("No departments in this hospital.")
        return

    dept_map = {d.name: d for d in departments}
    selected_dept = dept_map[
        st.selectbox("🏢 Select Department", dept_map.keys())
    ]

    st.markdown("---")

    with st.form("patient_registration_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *")
        with col2:
            last_name = st.text_input("Last Name *")

        col1, col2 = st.columns(2)
        with col1:
            date_of_birth = st.date_input(
                "Date of Birth *",
                value=datetime.now().date() - timedelta(days=365 * 30),
                min_value=datetime(1900, 1, 1).date(),
                max_value=datetime.now().date(),
            )
        with col2:
            age = calculate_age(date_of_birth)
            st.metric("Calculated Age", f"{age} years")

        phone = st.text_input("Phone Number *")
        medical_record = st.text_area("Medical Record (optional)")

        submitted = st.form_submit_button("✅ Register Patient", use_container_width=True)

    if submitted:
        try:
            patient_id = patient_repo.create(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                date_of_birth=date_of_birth,
                age=age,
                phone=phone.strip(),
                department_id=selected_dept.department_id,
                medical_record=medical_record.strip() or None,
            )

            st.success("✅ Patient registered successfully")
            st.info(f"Patient ID: {patient_id}")

        except Exception as e:
            st.error(f"❌ {e}")
            logger.exception("Patient registration failed")
