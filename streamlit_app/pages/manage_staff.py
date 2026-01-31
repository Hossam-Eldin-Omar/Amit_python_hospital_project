"""
Manage Staff page – create, view, and delete staff members
linked to a specific hospital department.

Flow: select Hospital → select Department → add/view staff
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.hospital_repository import HospitalRepository
from src.database.repositories.department_repository import DepartmentRepository
from src.database.repositories.staff_repository import StaffRepository
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
            StaffRepository(session=session),
        )
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None, None, None


def render():
    st.markdown("# 👔 Manage Staff")
    st.markdown("Add and manage staff members within hospital departments")
    st.markdown("---")

    hosp_repo, dept_repo, staff_repo = get_repos()
    if hosp_repo is None:
        st.error("⚠️ Unable to connect to database.")
        return

    # ─────────────────────────── Step 1: Pick Hospital ── #
    hospitals = hosp_repo.get_all() or []
    if not hospitals:
        st.warning("⚠️ No hospitals exist. Create one first via **Manage Hospitals**.")
        return

    hospital_map = {h.name: h for h in hospitals}
    selected_hospital_name = st.selectbox("🏥 Select Hospital", list(hospital_map.keys()))
    selected_hospital = hospital_map[selected_hospital_name]

    # ─────────────────────────── Step 2: Pick Department ── #
    departments = dept_repo.find_by_hospital(selected_hospital.hospital_id) or []
    if not departments:
        st.warning(
            f"⚠️ No departments in **{selected_hospital_name}**. "
            "Create one first via **Manage Departments**."
        )
        return

    dept_map = {d.name: d for d in departments}
    selected_dept_name = st.selectbox("🏢 Select Department", list(dept_map.keys()))
    selected_dept = dept_map[selected_dept_name]

    st.markdown("---")

    # ─────────────────────────── ADD Staff ──────────────── #
    st.markdown("### ➕ Add New Staff Member")
    with st.form("staff_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Mohamed")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Ali")

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age *", min_value=18, max_value=80, value=35)
        with col2:
            position = st.selectbox(
                "Position *",
                options=[
                    "Doctor", "Senior Doctor", "Specialist",
                    "Nurse", "Senior Nurse", "Head Nurse",
                    "Technician", "Lab Technician", "Receptionist",
                    "Other",
                ],
            )

        submitted = st.form_submit_button("✅ Add Staff Member", use_container_width=True)

    if submitted:
        errors = []
        if not first_name or not first_name.strip():
            errors.append("First name is required")
        if not last_name or not last_name.strip():
            errors.append("Last name is required")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            with st.spinner("Adding staff member…"):
                sid = staff_repo.create(
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    age=age,
                    position=position,
                    department_id=selected_dept.department_id,
                )
            if sid:
                st.success(
                    f"✅ **{first_name} {last_name}** added as **{position}** "
                    f"in {selected_dept_name}! (ID: {sid[:8]}…)"
                )
            else:
                st.error("❌ Failed to add staff member.")

    st.markdown("---")

    # ─────────────────────────── VIEW Staff ─────────────── #
    st.markdown(f"### 📋 Staff in {selected_dept_name}")
    staff_list = staff_repo.find_by_department(selected_dept.department_id) or []

    if not staff_list:
        st.info("No staff in this department yet.")
    else:
        rows = []
        for s in staff_list:
            rows.append(
                {
                    "Staff ID": str(s.staff_id)[:8] + "…",
                    "Name": f"{s.first_name} {s.last_name}",
                    "Position": s.position,
                    "Age": s.age,
                    "Department": selected_dept_name,
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ──────────────────────── DELETE ──────────────────────── #
        st.markdown("---")
        st.markdown("### 🗑️ Remove Staff Member")
        staff_names = {f"{s.first_name} {s.last_name} ({s.position})": s for s in staff_list}
        selected_staff_label = st.selectbox("Select staff to remove", list(staff_names.keys()))

        if st.button("🗑️ Remove Selected Staff", use_container_width=True):
            s = staff_names[selected_staff_label]
            if staff_repo.delete(s.department_id, s.staff_id):
                st.success(f"✅ Staff member removed.")
            else:
                st.error("❌ Removal failed.")

    # ─────────────────────────── Search across all ─── #
    st.markdown("---")
    with st.expander("🔍 Search Staff by Name (across all departments)"):
        col1, col2 = st.columns(2)
        with col1:
            s_first = st.text_input("First Name", key="staff_search_fn")
        with col2:
            s_last = st.text_input("Last Name", key="staff_search_ln")

        if s_first or s_last:
            results = staff_repo.find_by_name(s_first or None, s_last or None)
            if results:
                rows = []
                for s in results:
                    dept = dept_repo.find_by_id(s.department_id)
                    rows.append(
                        {
                            "Name": f"{s.first_name} {s.last_name}",
                            "Position": s.position,
                            "Age": s.age,
                            "Department": dept.name if dept else str(s.department_id)[:8] + "…",
                        }
                    )
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.warning("No staff found.")
