"""
Search Patients page – search and view patient details.
Results now include the department name resolved via DepartmentRepository.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.department_repository import DepartmentRepository
from src.database.repositories.patient_repository import PatientRepository
from src.database.repositories.hospital_repository import HospitalRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@st.cache_resource
def get_repos():
    try:
        from src.database.connection import ScyllaDBConnection
        from src.database.init_db import initialize_database

        db = ScyllaDBConnection()
        session = db.connect()
        initialize_database(session)
        return (
            DepartmentRepository(session=session),
            PatientRepository(session=session),
            HospitalRepository(session=session),
        )
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None, None


def _resolve_dept_name(dept_repo, department_id) -> str:
    """Look up department name; return short ID on miss."""
    dept = dept_repo.find_by_id(department_id)
    return dept.name if dept else str(department_id)[:8] + "…"

def _resolve_hosp_name(hosp_repo, hospital_id) -> str:
    """Look up hospital name; return short ID on miss."""
    hosp = hosp_repo.find_by_id(hospital_id)
    return hosp.name if hosp else str(hospital_id)[:8] + "…"


def render():
    st.markdown("# 🔍 Search Patients")
    st.markdown("Find and view patient details")
    st.markdown("---")

    dept_repo, patient_repo, hosp_repo = get_repos()
    if patient_repo is None:
        st.error("⚠️ Unable to connect to database.")
        return

    # ─────────────────────────── Search options ─── #
    search_type = st.radio(
        "Search by:",
        options=["View by hospital", "Patient ID", "Name", "Phone", "View All"],
        horizontal=True,
    )
    st.markdown("---")

    search_results = None
    if search_type == "View by hospital":
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

        with st.spinner("Loading patients…"):
            search_results = patient_repo.find_by_department(selected_dept.department_id) or []
        if not search_results:
            st.info("No patients in this department yet.")
    if search_type == "Patient ID":
        patient_id = st.text_input(
            "Enter Patient ID",
            placeholder="e.g. 12345678-1234-1234-1234-123456789012",
        )
        if patient_id:
            with st.spinner("Searching…"):
                result = patient_repo.find_by_id(patient_id)
            if result:
                search_results = [result]
            else:
                st.warning(f"❌ No patient found with ID: {patient_id}")

    elif search_type == "Name":
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Ahmed")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Hassan")

        if first_name or last_name:
            with st.spinner("Searching…"):
                search_results = patient_repo.find_by_name(
                    first_name or None, last_name or None
                )
            if not search_results:
                st.warning(f"❌ No patients found matching: {first_name} {last_name}")

    elif search_type == "Phone":
        phone = st.text_input("Phone Number", placeholder="+20 123-4567890")
        if phone:
            with st.spinner("Searching…"):
                all_p = patient_repo.get_all() or []
                search_results = [p for p in all_p if p.phone == phone]
            if not search_results:
                st.warning(f"❌ No patient with phone: {phone}")

    elif search_type == "View All":
        with st.spinner("Loading…"):
            search_results = patient_repo.get_all() or []
        if not search_results:
            st.info("No patients in the system yet.")

    # ─────────────────────────── Display results ─── #
    if search_results:
        st.markdown(
            f"### 📋 Results ({len(search_results)} patient{'s' if len(search_results) != 1 else ''})"
        )

        tab1, tab2 = st.tabs(["Table View", "Detailed View"])

        with tab1:
            rows = []
            for p in search_results:
                rows.append(
                    {
                        "ID": str(p.patient_id)[:8] + "…",
                        "First Name": p.first_name,
                        "Last Name": p.last_name,
                        "Age": p.age,
                        "Phone": p.phone,
                        "DOB": p.date_of_birth,
                        "Department": _resolve_dept_name(dept_repo, p.department_id),
                        "Hospital": _resolve_hosp_name(hosp_repo, dept_repo.find_by_id(p.department_id).hospital_id) if dept_repo.find_by_id(p.department_id) else "—",
                        "Medical Record": p.medical_record or "—",
                        "Registered": p.created_at,
                    }
                )
            st.dataframe(
                pd.DataFrame(rows), use_container_width=True, hide_index=True
            )

        with tab2:
            for i, p in enumerate(search_results):
                dept_name = _resolve_dept_name(dept_repo, p.department_id)
                hosp_name = _resolve_hosp_name(hosp_repo, dept_repo.find_by_id(p.department_id).hospital_id) if dept_repo.find_by_id(p.department_id) else "—"
                with st.expander(
                    f"👤 {p.first_name} {p.last_name} (ID: {str(p.patient_id)[:8]}…)",
                    expanded=(i == 0),
                ):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("**Personal Information**")
                        st.write(f"**First Name:** {p.first_name}")
                        st.write(f"**Last Name:** {p.last_name}")
                        st.write(f"**Age:** {p.age} years")
                        st.write(f"**DOB:** {p.date_of_birth}")
                    with col2:
                        st.markdown("**Contact & Department**")
                        st.write(f"**Phone:** {p.phone}")
                        st.write(f"**Department:** {dept_name}")
                        st.write(f"**Hospital:** {hosp_name}")
                        st.write(f"**Dept ID:** {str(p.department_id)[:8]}…")
                    with col3:
                        st.markdown("**Medical & System Info**")
                        st.write(f"**Medical Record:** {p.medical_record or '—'}")
                        st.write(f"**Patient ID:** {p.patient_id}")
                        st.write(f"**Registered:** {p.created_at}")

                    st.markdown("---")
                    a1, a2, a3 = st.columns(3)
                    with a1:
                        if st.button("📝 Edit", key=f"edit_{i}", use_container_width=True):
                            st.info("Edit functionality coming soon…")
                    with a2:
                        if st.button("📄 Full Record", key=f"view_{i}", use_container_width=True):
                            st.info("Full record view coming soon…")
                    with a3:
                        if st.button("🗑️ Delete", key=f"del_{i}", use_container_width=True):
                            if patient_repo.delete(p.department_id, p.patient_id):
                                st.success("✅ Patient deleted.")
                            else:
                                st.error("❌ Deletion failed.")

    # Tips
    with st.expander("💡 Search Tips"):
        st.markdown(
            "- **Patient ID:** use the full UUID\n"
            "- **Name:** search by first, last, or both\n"
            "- **Phone:** enter the exact phone number\n"
            "- **View All:** lists every patient (may be slow on large datasets)"
        )
