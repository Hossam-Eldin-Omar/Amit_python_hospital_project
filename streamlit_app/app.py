"""
Hospital Management System - Streamlit Web Application
Main entry point for the Streamlit application with navigation
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Hospital Management System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        
        /* Header styling */
        h1 {
            color: #1f77b4;
            text-align: center;
            padding: 2rem 0;
            border-bottom: 3px solid #1f77b4;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #1f77b4;
            margin-top: 2rem;
        }
        
        /* Card styling */
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #1557a0;
        }
        
        /* Success message */
        .success {
            color: #27ae60;
            font-weight: bold;
        }
        
        /* Error message */
        .error {
            color: #e74c3c;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("# 🏥 Hospital System")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        options=["Dashboard", "Add Patient", "Search Patients", "Settings"],
        help="Select a page to navigate"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "### About\n"
        "Hospital Management System v1.0\n\n"
        "Built with Streamlit & ScyllaDB"
    )
    
    # Route pages
    if page == "Dashboard":
        from pages import dashboard
        dashboard.render()
    
    elif page == "Add Patient":
        from pages import add_patient
        add_patient.render()
    
    elif page == "Search Patients":
        from pages import search_patient
        search_patient.render()
    
    elif page == "Settings":
        from pages import settings
        settings.render()


if __name__ == "__main__":
    main()
