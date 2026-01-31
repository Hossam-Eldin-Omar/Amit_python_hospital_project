"""
Manage Hospitals page – create, view, and delete hospitals.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.hospital_repository import HospitalRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@st.cache_resource
def get_repo():
    try:
        from src.database.connection import ScyllaDBConnection
        from src.database.init_db import initialize_database

        db = ScyllaDBConnection()
        session = db.connect()
        initialize_database(session)
        return HospitalRepository(session=session)
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None


def render():
    st.markdown("# 🏥 Manage Hospitals")
    st.markdown("Create and manage hospital entries")
    st.markdown("---")

    repo = get_repo()
    if repo is None:
        st.error("⚠️ Unable to connect to database.")
        return

    # ─────────────────────────── ADD ─────────────────────────── #
    st.markdown("### ➕ Add New Hospital")
    with st.form("hospital_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Hospital Name *", placeholder="e.g. Cairo Medical Center")
        with col2:
            location = st.text_input("Location *", placeholder="e.g. Tahrir, Cairo")
        phone = st.text_input("Phone (optional)", placeholder="+20 2 XXXX-XXXX")
        submitted = st.form_submit_button("✅ Create Hospital", use_container_width=True)

    if submitted:
        errors = []
        if not name or not name.strip():
            errors.append("Hospital name is required")
        if not location or not location.strip():
            errors.append("Location is required")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            with st.spinner("Creating hospital…"):
                hid = repo.create(name.strip(), location.strip(), phone.strip() or None)
            if hid:
                st.success(f"✅ Hospital created! ID: {hid}")
            else:
                st.error("❌ Failed to create hospital.")

    st.markdown("---")

    # ──────────────────────── VIEW ALL ──────────────────────── #
    st.markdown("### 📋 All Hospitals")
    hospitals = repo.get_all() or []

    if not hospitals:
        st.info("No hospitals registered yet.")
        return

    rows = []
    for h in hospitals:
        rows.append(
            {
                "Hospital ID": str(h.hospital_id),
                "Name": h.name,
                "Location": h.location,
                "Phone": h.phone or "—",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ──────────────────────── DELETE ──────────────────────── #
    st.markdown("---")
    st.markdown("### 🗑️ Delete Hospital")
    hospital_names = {h.name: h for h in hospitals}
    selected = st.selectbox("Select hospital to delete", list(hospital_names.keys()))

    if st.button("🗑️ Delete Selected Hospital", use_container_width=True):
        h = hospital_names[selected]
        if repo.delete(h.hospital_id):
            st.success(f"✅ Hospital '{selected}' deleted.")
        else:
            st.error("❌ Deletion failed.")
