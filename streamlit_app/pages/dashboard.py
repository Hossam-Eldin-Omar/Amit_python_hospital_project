"""
Dashboard page – displays live hospital statistics across all four entities.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.hospital_repository import HospitalRepository
from src.database.repositories.department_repository import DepartmentRepository
from src.database.repositories.patient_repository import PatientRepository
from src.database.repositories.staff_repository import StaffRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


# ─────────────────────────────────────────────────────────── #
# Cached repo accessors
# ─────────────────────────────────────────────────────────── #
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
            PatientRepository(session=session),
            StaffRepository(session=session),
        )
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None, None, None, None


def render():
    st.markdown("# 📊 Dashboard")
    st.markdown("Live overview of the entire hospital system")
    st.markdown("---")

    hosp_repo, dept_repo, patient_repo, staff_repo = get_repos()
    if hosp_repo is None:
        st.error("⚠️ Unable to connect to database.")
        return

    # ───── Fetch all data ───── #
    hospitals = hosp_repo.get_all() or []
    departments = dept_repo.get_all() or []
    patients = patient_repo.get_all() or []
    staff = staff_repo.get_all() or []

    # ───── Top-level metrics ───── #
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏥 Hospitals", len(hospitals))
    with col2:
        st.metric("🏢 Departments", len(departments))
    with col3:
        st.metric("👥 Patients", len(patients))
    with col4:
        st.metric("👔 Staff", len(staff))

    st.markdown("---")

    # ───── Charts ───── #
    col_left, col_right = st.columns(2)

    # Patients per department (pie)
    with col_left:
        st.markdown("### 👥 Patients by Department")
        dept_patient_counts = {}
        for d in departments:
            dept_patient_counts[d.name] = len(
                patient_repo.find_by_department(d.department_id)
            )

        if dept_patient_counts:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=list(dept_patient_counts.keys()),
                        values=list(dept_patient_counts.values()),
                        marker=dict(
                            colors=[
                                "#FF6B6B", "#4ECDC4", "#45B7D1",
                                "#FFA07A", "#98D8C8", "#7B68EE",
                            ]
                        ),
                    )
                ]
            )
            fig.update_layout(height=350, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No department data yet.")

    # Staff per department (bar)
    with col_right:
        st.markdown("### 👔 Staff by Department")
        dept_staff_counts = {}
        for d in departments:
            dept_staff_counts[d.name] = len(
                staff_repo.find_by_department(d.department_id)
            )

        if dept_staff_counts:
            fig_bar = px.bar(
                x=list(dept_staff_counts.keys()),
                y=list(dept_staff_counts.values()),
                labels={"x": "Department", "y": "Staff Count"},
                color_discrete_sequence=["#667eea"],
            )
            fig_bar.update_layout(height=350, template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No staff data yet.")

    st.markdown("---")

    # ───── Departments per hospital (bar) ───── #
    st.markdown("### 🏥 Departments per Hospital")
    hosp_dept_counts = {}
    for h in hospitals:
        hosp_dept_counts[h.name] = len(dept_repo.find_by_hospital(h.hospital_id))

    if hosp_dept_counts:
        fig_h = px.bar(
            x=list(hosp_dept_counts.keys()),
            y=list(hosp_dept_counts.values()),
            labels={"x": "Hospital", "y": "Departments"},
            color_discrete_sequence=["#4ECDC4"],
        )
        fig_h.update_layout(height=300, template="plotly_white")
        st.plotly_chart(fig_h, use_container_width=True)
    else:
        st.info("No hospital data yet.")

    st.markdown("---")

    # ───── Recent patients table ───── #
    st.markdown("### 📋 Recent Patients")
    if patients:
        rows = []
        for p in patients[:15]:
            rows.append(
                {
                    "Patient ID": str(p.patient_id)[:8] + "...",
                    "Name": f"{p.first_name} {p.last_name}",
                    "Age": p.age,
                    "Phone": p.phone,
                    "Department": str(p.department_id)[:8] + "...",
                    "Medical Record": p.medical_record or "—",
                    "Registered": p.created_at,
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No patients registered yet.")

    st.markdown("---")

    # ───── Recent staff table ───── #
    st.markdown("### 📋 Staff Members")
    if staff:
        rows = []
        for s in staff[:15]:
            rows.append(
                {
                    "Staff ID": str(s.staff_id)[:8] + "...",
                    "Name": f"{s.first_name} {s.last_name}",
                    "Position": s.position,
                    "Age": s.age,
                    "Department": str(s.department_id)[:8] + "...",
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No staff registered yet.")
