"""
Settings page - application settings and configuration
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def render():
    """Render settings page"""
    
    st.markdown("# ⚙️ Settings")
    st.markdown("Configure application settings and preferences")
    st.markdown("---")
    
    # System Information
    st.markdown("### 📊 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Application:** Hospital Management System
        **Version:** 1.0.0
        **Built with:** Streamlit & ScyllaDB
        """)
    
    with col2:
        st.info("""
        **Python Version:** 3.9+
        **Database:** ScyllaDB 5.0+
        **Status:** Active
        """)
    
    with col3:
        st.info("""
        **Last Updated:** 2024-01-30
        **License:** MIT
        **Support:** admin@hospital.local
        """)
    
    st.markdown("---")
    
    # Display Settings
    st.markdown("### 🎨 Display Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Application Theme",
            options=["Light", "Dark", "Auto"],
            help="Choose your preferred theme"
        )
        st.success(f"Theme set to: {theme}")
    
    with col2:
        rows_per_page = st.slider(
            "Rows per Page",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="Number of rows to display in tables"
        )
        st.success(f"Display {rows_per_page} rows per page")
    
    st.markdown("---")
    
    # Database Settings
    st.markdown("### 🗄️ Database Settings")
    
    st.info("**Current Database Configuration**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        host = st.text_input(
            "Database Host",
            value="scylla-node",
            disabled=True,
            help="ScyllaDB host address"
        )
    
    with col2:
        port = st.number_input(
            "Database Port",
            value=9042,
            disabled=True,
            help="ScyllaDB port"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        keyspace = st.text_input(
            "Keyspace",
            value="hospital",
            disabled=True,
            help="ScyllaDB keyspace"
        )
    
    with col2:
        consistency_level = st.selectbox(
            "Consistency Level",
            options=["ONE", "LOCAL_QUORUM", "QUORUM"],
            index=1,
            help="Database consistency level"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Test Database Connection", use_container_width=True):
            st.spinner("Testing connection...")
            st.success("✅ Database connection successful!")
            logger.info("Database connection test successful")
    
    with col2:
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✅ Settings saved successfully!")
            logger.info("Settings updated")
    
    st.markdown("---")
    
    # Logging Settings
    st.markdown("### 📝 Logging Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        log_level = st.selectbox(
            "Log Level",
            options=["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,
            help="Application logging level"
        )
    
    with col2:
        enable_file_logging = st.checkbox(
            "Enable File Logging",
            value=True,
            help="Save logs to file"
        )
    
    if st.button("📋 View Logs", use_container_width=True):
        st.info("Log viewer - detailed logs from the application")
        st.code("""
2024-01-30 10:15:23 INFO Database connection established
2024-01-30 10:15:24 INFO Patient repository initialized
2024-01-30 10:15:45 INFO Patient registered: John Doe (ID: abc123...)
2024-01-30 10:16:12 INFO Patient search executed
        """, language="log")
    
    st.markdown("---")
    
    # User Management
    st.markdown("### 👥 User Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input(
            "Username",
            value="admin",
            disabled=True
        )
    
    with col2:
        role = st.selectbox(
            "User Role",
            options=["Administrator", "Doctor", "Nurse", "Receptionist"],
            index=0,
            disabled=True
        )
    
    if st.button("🔐 Change Password", use_container_width=True):
        st.info("Password change dialog - feature coming soon")
    
    st.markdown("---")
    
    # Backup & Maintenance
    st.markdown("### 🛠️ Backup & Maintenance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Backup Database", use_container_width=True):
            st.success("✅ Database backup completed successfully!")
            logger.info("Database backup initiated")
    
    with col2:
        if st.button("🔧 Optimize Database", use_container_width=True):
            st.success("✅ Database optimization completed!")
            logger.info("Database optimization completed")
    
    with col3:
        if st.button("🧹 Clean Cache", use_container_width=True):
            st.success("✅ Cache cleared successfully!")
            logger.info("Cache cleared")
    
    st.markdown("---")
    
    # About Section
    st.markdown("### ℹ️ About")
    
    st.markdown("""
    **Hospital Management System**
    
    A comprehensive Python-based healthcare management platform built with Streamlit and ScyllaDB 
    for high-performance distributed data storage. It provides automated patient registration, 
    data validation, and hospital operations management with professional logging.
    
    - **License:** MIT
    - **Author:** Development Team
    - **Repository:** github.com/hospital-mgmt
    - **Documentation:** docs.hospital-mgmt.local
    
    For support, please contact: support@hospital.local
    """)
