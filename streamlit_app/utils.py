"""
Streamlit utilities - helper functions and custom components
"""

import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd


def apply_custom_css():
    """Apply custom CSS styling to Streamlit app"""
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #f5f7fa;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        /* Headers */
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        
        h3 {
            color: #667eea;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background-color: #764ba2;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }
        
        /* Text input */
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 2px solid #e0e0e0;
            padding: 10px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        
        /* Selectbox */
        .stSelectbox > div > div > select {
            border-radius: 5px;
            border: 2px solid #e0e0e0;
        }
        
        /* Cards / Info boxes */
        .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 5px;
            border-left: 4px solid;
        }
        
        .stInfo {
            background-color: #e3f2fd;
            border-left-color: #2196f3;
        }
        
        .stSuccess {
            background-color: #e8f5e9;
            border-left-color: #4caf50;
        }
        
        .stWarning {
            background-color: #fff3e0;
            border-left-color: #ff9800;
        }
        
        .stError {
            background-color: #ffebee;
            border-left-color: #f44336;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem;
            color: #667eea;
            font-weight: bold;
        }
        
        /* Dataframe */
        .stDataFrame {
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1rem;
            font-weight: 600;
        }
        
        /* Expander */
        .stExpander {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }
        
        /* Code block */
        .stCodeBlock {
            border-radius: 5px;
        }
        
        /* Divider */
        hr {
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)


def create_metric_card(title: str, value: Any, subtitle: str = "") -> None:
    """Create a styled metric card"""
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h3 style="margin: 0; font-size: 1.2rem;">{title}</h3>
            <p style="margin: 10px 0 0 0; font-size: 2.5rem; font-weight: bold;">{value}</p>
            {f'<p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def format_patient_data(patient_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Format patient data for display"""
    return {
        'patient_id': str(patient_dict.get('patient_id', 'N/A'))[:8] + '...',
        'first_name': patient_dict.get('first_name', 'N/A'),
        'last_name': patient_dict.get('last_name', 'N/A'),
        'age': patient_dict.get('age', 'N/A'),
        'phone': patient_dict.get('phone', 'N/A'),
        'date_of_birth': patient_dict.get('date_of_birth', 'N/A'),
        'created_at': patient_dict.get('created_at', 'N/A')
    }


def create_patient_dataframe(patients: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create formatted DataFrame from patient list"""
    formatted_patients = [format_patient_data(p) for p in patients]
    return pd.DataFrame(formatted_patients)


def show_success_banner(message: str) -> None:
    """Display a success banner"""
    st.markdown(f"""
        <div style="
            background-color: #4caf50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        ">
            ✅ {message}
        </div>
    """, unsafe_allow_html=True)


def show_error_banner(message: str) -> None:
    """Display an error banner"""
    st.markdown(f"""
        <div style="
            background-color: #f44336;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        ">
            ❌ {message}
        </div>
    """, unsafe_allow_html=True)


def show_warning_banner(message: str) -> None:
    """Display a warning banner"""
    st.markdown(f"""
        <div style="
            background-color: #ff9800;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        ">
            ⚠️ {message}
        </div>
    """, unsafe_allow_html=True)


def show_info_banner(message: str) -> None:
    """Display an info banner"""
    st.markdown(f"""
        <div style="
            background-color: #2196f3;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        ">
            ℹ️ {message}
        </div>
    """, unsafe_allow_html=True)


def render_patient_card(patient: Dict[str, Any], show_actions: bool = False) -> None:
    """Render a patient information card"""
    st.markdown(f"""
        <div style="
            background: white;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 15px 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #2c3e50;">
                        {patient.get('first_name', 'N/A')} {patient.get('last_name', 'N/A')}
                    </h4>
                    <p style="margin: 5px 0; color: #667eea; font-weight: 600;">
                        ID: {patient.get('patient_id', 'N/A')}
                    </p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0; font-size: 1.5rem; color: #667eea; font-weight: bold;">
                        {patient.get('age', 'N/A')} yrs
                    </p>
                </div>
            </div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #e0e0e0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #666;">📅 DOB</p>
                    <p style="margin: 0; font-weight: 600;">{patient.get('date_of_birth', 'N/A')}</p>
                </div>
                <div>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #666;">📞 Phone</p>
                    <p style="margin: 0; font-weight: 600;">{patient.get('phone', 'N/A')}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


@st.cache_data
def get_sample_dashboard_data():
    """Get sample data for dashboard"""
    return {
        'total_patients': 156,
        'active_today': 12,
        'departments': 5,
        'system_health': '100%'
    }
