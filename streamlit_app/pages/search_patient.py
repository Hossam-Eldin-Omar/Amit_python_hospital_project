"""
Search Patients page - search and view patient details
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.repositories.patient_repository import PatientRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@st.cache_resource
def get_patient_repository():
    """Get or create PatientRepository instance"""
    try:
        return PatientRepository()
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None


def render():
    """Render search patients page"""
    
    st.markdown("# 🔍 Search Patients")
    st.markdown("Find and view patient details")
    st.markdown("---")
    
    repo = get_patient_repository()
    
    if repo is None:
        st.error("⚠️ Unable to connect to database. Please check your database configuration.")
        return
    
    # Search options
    search_type = st.radio(
        "Search by:",
        options=["Patient ID", "Name", "Phone", "View All"],
        horizontal=True,
        help="Select how you want to search for patients"
    )
    
    st.markdown("---")
    
    search_results = None
    
    if search_type == "Patient ID":
        patient_id = st.text_input(
            "Enter Patient ID",
            placeholder="e.g., 12345678-1234-1234-1234-123456789012",
            help="Enter the patient's unique ID"
        )
        
        if patient_id:
            try:
                with st.spinner("Searching..."):
                    search_results = repo.find_by_id(patient_id)
                
                if search_results:
                    search_results = [search_results]
                else:
                    st.warning(f"❌ No patient found with ID: {patient_id}")
            
            except Exception as e:
                logger.error(f"Error searching by ID: {e}")
                st.error(f"Error searching: {str(e)}")
    
    elif search_type == "Name":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            first_name = st.text_input(
                "First Name",
                placeholder="Enter first name",
                help="Enter patient's first name (partial match supported)"
            )
        
        with col2:
            last_name = st.text_input(
                "Last Name",
                placeholder="Enter last name",
                help="Enter patient's last name (partial match supported)"
            )
        
        if first_name or last_name:
            try:
                with st.spinner("Searching..."):
                    search_results = repo.find_by_name(first_name, last_name)
                
                if not search_results:
                    st.warning(f"❌ No patients found matching: {first_name} {last_name}")
            
            except Exception as e:
                logger.error(f"Error searching by name: {e}")
                st.error(f"Error searching: {str(e)}")
    
    elif search_type == "Phone":
        phone = st.text_input(
            "Phone Number",
            placeholder="+1 (555) 123-4567",
            help="Enter patient's phone number"
        )
        
        if phone:
            try:
                with st.spinner("Searching..."):
                    all_patients = repo.get_all()
                    search_results = [p for p in all_patients if p.phone == phone] if all_patients else []
                
                if not search_results:
                    st.warning(f"❌ No patient found with phone: {phone}")
            
            except Exception as e:
                logger.error(f"Error searching by phone: {e}")
                st.error(f"Error searching: {str(e)}")
    
    elif search_type == "View All":
        try:
            with st.spinner("Loading all patients..."):
                search_results = repo.get_all()
            
            if not search_results:
                st.info("ℹ️ No patients in the system yet.")
        
        except Exception as e:
            logger.error(f"Error fetching all patients: {e}")
            st.error(f"Error loading patients: {str(e)}")
    
    # Display search results
    if search_results:
        st.markdown(f"### 📋 Results ({len(search_results)} patient{'s' if len(search_results) != 1 else ''})")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Table View", "Detailed View"])
        
        with tab1:
            # Table view
            patient_data = []
            for patient in search_results:
                patient_dict = patient.to_dict() if hasattr(patient, 'to_dict') else patient
                patient_data.append({
                    'ID': str(patient_dict.get('patient_id', 'N/A'))[:8] + '...',
                    'First Name': patient_dict.get('first_name', 'N/A'),
                    'Last Name': patient_dict.get('last_name', 'N/A'),
                    'Age': patient_dict.get('age', 'N/A'),
                    'Phone': patient_dict.get('phone', 'N/A'),
                    'DOB': patient_dict.get('date_of_birth', 'N/A'),
                    'Registered': patient_dict.get('created_at', 'N/A')
                })
            
            df = pd.DataFrame(patient_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab2:
            # Detailed view with expandable cards
            for i, patient in enumerate(search_results):
                patient_dict = patient.to_dict() if hasattr(patient, 'to_dict') else patient
                with st.expander(
                    f"👤 {patient_dict.get('first_name', 'N/A')} {patient_dict.get('last_name', 'N/A')} "
                    f"(ID: {str(patient_dict.get('patient_id', 'N/A'))[:8]}...)",
                    expanded=(i == 0)  # Expand first result by default
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Personal Information**")
                        st.write(f"**First Name:** {patient_dict.get('first_name', 'N/A')}")
                        st.write(f"**Last Name:** {patient_dict.get('last_name', 'N/A')}")
                        st.write(f"**Age:** {patient_dict.get('age', 'N/A')} years")
                    
                    with col2:
                        st.markdown("**Contact Information**")
                        st.write(f"**Phone:** {patient_dict.get('phone', 'N/A')}")
                        st.write(f"**DOB:** {patient_dict.get('date_of_birth', 'N/A')}")
                        st.write(f"**Email:** N/A")
                    
                    with col3:
                        st.markdown("**System Information**")
                        st.write(f"**Patient ID:** {patient_dict.get('patient_id', 'N/A')}")
                        st.write(f"**Department:** {patient_dict.get('department_id', 'N/A')}")
                        st.write(f"**Registered:** {patient_dict.get('created_at', 'N/A')}")
                    
                    st.markdown("---")
                    
                    # Action buttons
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    with action_col1:
                        if st.button("📝 Edit", key=f"edit_{i}", use_container_width=True):
                            st.info("Edit functionality coming soon...")
                    
                    with action_col2:
                        if st.button("📄 View Full Record", key=f"view_{i}", use_container_width=True):
                            st.info("Full record view coming soon...")
                    
                    with action_col3:
                        if st.button("🗑️ Delete", key=f"delete_{i}", use_container_width=True):
                            st.warning("Delete functionality - confirm action needed")
    
    # Search tips
    with st.expander("💡 Search Tips"):
        st.markdown("""
        - **Patient ID Search:** Use the full or partial patient ID
        - **Name Search:** Search by first name, last name, or both
        - **Phone Search:** Enter the complete phone number
        - **View All:** Display all patients in the system (may be slow with large datasets)
        - **Partial Matching:** Name searches support partial matches
        """)
