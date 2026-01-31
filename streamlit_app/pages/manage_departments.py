"""
Manage Departments page – create, view, and delete departments
linked to their parent hospital.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.hospital_repository import HospitalRepository
from src.database.repositories.department_repository import DepartmentRepository
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
            HospitalRepository(session=session),
            DepartmentRepository(session=session),
        )
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None, None


def render():
    st.markdown("# 🏢 Manage Departments")
    st.markdown("Create and manage departments within hospitals")
    st.markdown("---")

    hosp_repo, dept_repo = get_repos()
    if hosp_repo is None:
        st.error("⚠️ Unable to connect to database.")
        return

    hospitals = hosp_repo.get_all() or []
    if not hospitals:
        st.warning("⚠️ No hospitals exist yet. Create a hospital first via **Manage Hospitals**.")
        return

    # Hospital selector (used for both add & view)
    hospital_map = {h.name: h for h in hospitals}
    selected_hospital_name = st.selectbox(
        "Select Hospital", list(hospital_map.keys()), help="Filter departments by hospital"
    )
    selected_hospital = hospital_map[selected_hospital_name]

    st.markdown("---")

    # ─────────────────────────── ADD ─────────────────────────── #
    st.markdown("### ➕ Add New Department")
    with st.form("dept_form", clear_on_submit=True):
        dept_name = st.text_input("Department Name *", placeholder="e.g. Cardiology")
        description = st.text_input("Description (optional)", placeholder="Heart & vascular care")
        submitted = st.form_submit_button("✅ Create Department", use_container_width=True)

    if submitted:
        if not dept_name or not dept_name.strip():
            st.error("❌ Department name is required")
        else:
            with st.spinner("Creating department…"):
                did = dept_repo.create(
                    name=dept_name.strip(),
                    hospital_id=selected_hospital.hospital_id,
                    description=description.strip() or None,
                )
            if did:
                st.success(
                    f"✅ Department **{dept_name}** created in "
                    f"**{selected_hospital_name}**! (ID: {did})"
                )
            else:
                st.error("❌ Failed to create department.")

    st.markdown("---")

    # ──────────────────────── VIEW ──────────────────────── #
    st.markdown(f"### 📋 Departments in {selected_hospital_name}")
    departments = dept_repo.find_by_hospital(selected_hospital.hospital_id) or []

    if not departments:
        st.info("No departments in this hospital yet.")
    else:
        rows = []
        for d in departments:
            rows.append(
                {
                    "Department ID": str(d.department_id),
                    "Name": d.name,
                    "Description": d.description or "—",
                    "Hospital": selected_hospital_name,
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ──────────────────────── DELETE ──────────────────────── #
        st.markdown("---")
        st.markdown("### 🗑️ Delete Department")
        dept_map = {d.name: d for d in departments}
        selected_dept_name = st.selectbox("Select department to delete", list(dept_map.keys()))

        if st.button("🗑️ Delete Selected Department", use_container_width=True):
            d = dept_map[selected_dept_name]
            if dept_repo.delete(d.hospital_id, d.department_id):
                st.success(f"✅ Department '{selected_dept_name}' deleted.")
            else:
                st.error("❌ Deletion failed.")
