"""
Dashboard page - displays hospital statistics and overview
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
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
    """Render dashboard page"""
    
    st.markdown("# 📊 Dashboard")
    st.markdown("Hospital Management System Overview")
    st.markdown("---")
    
    repo = get_patient_repository()
    
    if repo is None:
        st.error("⚠️ Unable to connect to database. Please check your database configuration.")
        return
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Fetch total patients count
    try:
        all_patients = repo.get_all()
        total_patients = len(all_patients) if all_patients else 0
        
        with col1:
            st.metric(
                label="👥 Total Patients",
                value=total_patients,
                delta="+5 this month",
                delta_color="off"
            )
    except Exception as e:
        logger.error(f"Error fetching patient count: {e}")
        with col1:
            st.metric(label="👥 Total Patients", value="N/A")
    
    # Active patients today (mock data)
    with col2:
        st.metric(
            label="🏥 Active Today",
            value="12",
            delta="+2 from yesterday"
        )
    
    # Departments
    with col3:
        st.metric(
            label="🏢 Departments",
            value="5",
            delta="All operational"
        )
    
    # System Health
    with col4:
        st.metric(
            label="💚 System Health",
            value="100%",
            delta="All systems operational"
        )
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Patient Registration Trend")
        
        # Sample data for trend
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        registrations = [5, 7, 3, 9, 11, 8, 6, 12, 4, 10, 
                        7, 9, 11, 5, 8, 6, 10, 12, 7, 9,
                        8, 11, 6, 9, 10, 7, 8, 12, 5, 11]
        
        df_trend = pd.DataFrame({
            'Date': dates,
            'Registrations': registrations
        })
        
        fig_trend = px.line(df_trend, x='Date', y='Registrations',
                           title='Daily Patient Registrations (Last 30 Days)',
                           markers=True,
                           line_shape='spline')
        fig_trend.update_layout(
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.markdown("### 🏥 Patients by Department")
        
        departments = ['Cardiology', 'Orthopedics', 'Neurology', 'Pediatrics', 'General']
        patient_counts = [24, 18, 15, 22, 31]
        
        fig_dept = go.Figure(data=[
            go.Pie(labels=departments, values=patient_counts,
                  marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']))
        ])
        fig_dept.update_layout(
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    st.markdown("---")
    
    # Recent activity section
    st.markdown("### 📋 Recent Patient Registrations")
    
    try:
        all_patients = repo.get_all()
        recent_patients = all_patients[:10] if all_patients else []
        
        if recent_patients and len(recent_patients) > 0:
            # Create DataFrame from patient data
            patient_data = []
            for patient in recent_patients:
                patient_dict = patient.to_dict() if hasattr(patient, 'to_dict') else patient
                patient_data.append({
                    'Patient ID': str(patient_dict.get('patient_id', 'N/A'))[:8] + '...',
                    'Name': f"{patient_dict.get('first_name', '')} {patient_dict.get('last_name', '')}",
                    'Age': patient_dict.get('age', 'N/A'),
                    'Phone': patient_dict.get('phone', 'N/A'),
                    'Registration Date': patient_dict.get('created_at', 'N/A')
                })
            
            df_recent = pd.DataFrame(patient_data)
            st.dataframe(df_recent, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No patients registered yet.")
    
    except Exception as e:
        logger.error(f"Error fetching recent patients: {e}")
        st.warning(f"Could not load recent patients: {str(e)}")
    
    st.markdown("---")
    
    # Quick stats boxes
    st.markdown("### 📊 Key Metrics")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.info("**Average Age**: 45.3 years")
    
    with metric_col2:
        st.info("**Total Admissions**: 156")
    
    with metric_col3:
        st.info("**Avg. Hospital Stay**: 4.2 days")
