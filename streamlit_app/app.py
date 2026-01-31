"""
Hospital Management System – Streamlit Web Application
Single-page app with manual (view-based) navigation.
"""

import streamlit as st
from pathlib import Path
import sys

# Make src/ importable
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# ──────────────────────────────────────────────
# Page Config (MUST be first)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Hide Streamlit multipage menu
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Styling
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main { padding: 2rem; }

    [data-testid="stSidebar"] {
        background-color: #f0f4f8;
    }

    [data-testid="stSidebar"] .stButton > button {
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 0.92rem;
        text-align: left;
        padding-left: 12px !important;
        width: 100%;
    }

    [data-testid="stSidebar"] .stButton > button[type="secondary"] {
        background-color: transparent;
        color: #2c3e50;
        border: 1px solid transparent;
    }

    [data-testid="stSidebar"] .stButton > button[type="secondary"]:hover {
        background-color: #dce8f5;
        border-color: #aaccee;
    }

    [data-testid="stSidebar"] .stButton > button[type="primary"] {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none;
    }

    h1 {
        color: #1f77b4;
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Navigation Button
# ──────────────────────────────────────────────
def nav_button(label: str, page_key: str):
    active = st.session_state.get("current_page") == page_key

    if st.sidebar.button(
        label,
        key=f"nav_{page_key}",
        use_container_width=True,
        type="primary" if active else "secondary",
    ):
        st.session_state["current_page"] = page_key
        st.rerun()  # Refresh to reflect page change

# ──────────────────────────────────────────────
# Default Page
# ──────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "dashboard"

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
st.sidebar.markdown("# 🏥 Hospital System")
st.sidebar.markdown("---")

nav_button("📊 Dashboard", "dashboard")

st.sidebar.markdown("**🏥 Hospitals**")
nav_button("Manage Hospitals", "manage_hospitals")

st.sidebar.markdown("**🏢 Departments**")
nav_button("Manage Departments", "manage_departments")

st.sidebar.markdown("**🧑‍⚕️ Patients**")
nav_button("Add Patient", "add_patient")
nav_button("Search Patients", "search_patients")

st.sidebar.markdown("**👥 Staff**")
nav_button("Manage Staff", "manage_staff")

st.sidebar.markdown("**⚙️ System**")
nav_button("Settings", "settings")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Hospital Management System** v2.0\n\n"
    "Streamlit + ScyllaDB"
)

# ──────────────────────────────────────────────
# Router (Views)
# ──────────────────────────────────────────────
page = st.session_state["current_page"]

if page == "dashboard":
    from pages import dashboard
    dashboard.render()

elif page == "manage_hospitals":
    from pages import manage_hospitals
    manage_hospitals.render()

elif page == "manage_departments":
    from pages import manage_departments
    manage_departments.render()

elif page == "add_patient":
    from pages import add_patient
    add_patient.render()

elif page == "search_patients":
    from pages import search_patient
    search_patient.render()

elif page == "manage_staff":
    from pages import manage_staff
    manage_staff.render()

elif page == "settings":
    from pages import settings
    settings.render()

else:
    st.info("👈 Select a page from the sidebar.")
