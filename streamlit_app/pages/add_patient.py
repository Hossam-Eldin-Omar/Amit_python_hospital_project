"""
Add Patient page - form for registering new patients
"""

import streamlit as st
from datetime import datetime, timedelta
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


def calculate_age(dob):
    """Calculate age from date of birth"""
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def render():
    """Render add patient page"""
    
    st.markdown("# 👤 Add New Patient")
    st.markdown("Register a new patient in the hospital system")
    st.markdown("---")
    
    repo = get_patient_repository()
    
    if repo is None:
        st.error("⚠️ Unable to connect to database. Please check your database configuration.")
        return
    
    # Create a form for patient registration
    with st.form("patient_registration_form", clear_on_submit=True):
        
        st.markdown("### Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name *",
                placeholder="Enter first name",
                help="Patient's first name"
            )
        
        with col2:
            last_name = st.text_input(
                "Last Name *",
                placeholder="Enter last name",
                help="Patient's last name"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            date_of_birth = st.date_input(
                "Date of Birth *",
                value=datetime.now() - timedelta(days=365*30),
                min_value=datetime.now() - timedelta(days=365*120),
                max_value=datetime.now(),
                help="Patient's date of birth"
            )
        
        with col2:
            age = calculate_age(date_of_birth)
            st.metric(label="Calculated Age", value=f"{age} years")
        
        st.markdown("### Contact Information")
        
        phone = st.text_input(
            "Phone Number *",
            placeholder="+1 (555) 123-4567",
            help="Patient's contact phone number"
        )
        
        email = st.text_input(
            "Email (Optional)",
            placeholder="patient@example.com",
            help="Patient's email address"
        )
        
        st.markdown("### Additional Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox(
                "Gender",
                options=["Not Specified", "Male", "Female", "Other"],
                help="Patient's gender"
            )
        
        with col2:
            blood_type = st.selectbox(
                "Blood Type (Optional)",
                options=["Not Specified", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
                help="Patient's blood type"
            )
        
        st.markdown("---")
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            submitted = st.form_submit_button(
                "✅ Register Patient",
                use_container_width=True
            )
        
        with col2:
            st.form_submit_button(
                "🔄 Reset Form",
                use_container_width=True
            )
    
    # Handle form submission
    if submitted:
        # Validation
        validation_errors = []
        
        if not first_name or not first_name.strip():
            validation_errors.append("❌ First name is required")
        
        if not last_name or not last_name.strip():
            validation_errors.append("❌ Last name is required")
        
        if not phone or not phone.strip():
            validation_errors.append("❌ Phone number is required")
        
        # Phone validation (basic)
        if phone and not any(c.isdigit() for c in phone):
            validation_errors.append("❌ Phone number must contain at least one digit")
        
        if validation_errors:
            for error in validation_errors:
                st.error(error)
        else:
            # Attempt to register patient
            try:
                with st.spinner("🔄 Registering patient..."):
                    patient_id = repo.create(
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        date_of_birth=date_of_birth.strftime("%Y-%m-%d"),
                        age=age,
                        phone=phone.strip()
                    )
                
                if patient_id:
                    st.success(f"✅ Patient registered successfully!")
                    
                    # Display registration summary
                    st.markdown("### 📋 Registration Summary")
                    
                    summary_col1, summary_col2 = st.columns(2)
                    
                    with summary_col1:
                        st.info(f"**Patient ID:** {str(patient_id)[:8]}...")
                        st.info(f"**Name:** {first_name} {last_name}")
                        st.info(f"**Age:** {age} years")
                    
                    with summary_col2:
                        st.info(f"**DOB:** {date_of_birth.strftime('%B %d, %Y')}")
                        st.info(f"**Phone:** {phone}")
                        st.info(f"**Registered:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    
                    # Log the registration
                    logger.info(f"Patient registered: {first_name} {last_name} (ID: {patient_id})")
                else:
                    st.error("❌ Failed to register patient. Please try again.")
                    logger.error(f"Failed to register patient: {first_name} {last_name}")
            
            except Exception as e:
                st.error(f"❌ Error registering patient: {str(e)}")
                logger.error(f"Exception during patient registration: {e}")
    
    # Information section
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Required Fields:**
        - First Name
        - Last Name
        - Date of Birth
        - Phone Number
        
        The system will automatically:
        - Calculate patient age
        - Generate unique patient ID
        - Record registration timestamp
        """)
    
    with col2:
        st.markdown("""
        **Tips:**
        - Ensure phone number is valid
        - Use correct date format (MM/DD/YYYY)
        - Fill in blood type for emergency reference
        - Double-check information before submitting
        """)
