import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle 
import os
import requests
import subprocess
import time

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

BASE_DIR = os.getcwd()

backend = subprocess.Popen(["uvicorn", "main_fapi:app", "--port", "8000"])
backend.wait()

st.set_page_config(page_title = "Placement Prediction App", layout = "wide")
API_URL_BASE = 'http://127.0.0.1:8000/predict'

@st.cache_data
def get_api_info():
    try:
        res = requests.get(f"{API_URL_BASE}/info", timeout=5)
        return res.json()
    except:
        return None

info_res = get_api_info()

if info_res:
    # st.sidebar.write(f"Model: {info_res['details'][0]['name']}")
    st.sidebar.write(f"Model Aktif Berjalan!")
else:
    st.sidebar.error("Backend tidak terjangkau")

st.title("Student Placement Prediction")
st.write("Masukkan data mahasiswa di bawah ini untuk memprediksi status penempatan.")
# st.sidebar.write(f"Model: {info_res['details'][0]['name']}")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ['Male', 'Female'])
    ssc_percentage = st.number_input("SSC Percentage (10th)", 0, 100, 70)
    hsc_percentage = st.number_input("HSC Percentage (12th)", 0, 100, 70)
    degree_percentage = st.number_input("Degree Percentage", 0, 100, 70)
    cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0, step=0.1)

with col2:
    entrance_exam_score = st.number_input("Entrance Exam Score", 0, 100, 75)
    technical_skill_score = st.number_input("Technical Skill Score", 0, 100, 75)
    soft_skill_score = st.number_input("Soft Skill Score", 0, 100, 75)
    internship_count = st.number_input("Internship Count", 0, 10, 1)
    live_projects = st.number_input("Live Projects", 0, 10, 1)

with col3:
    work_experience_months = st.number_input("Work Experience (Months)", 0, 60, 0)
    certifications = st.number_input("Certifications Count", 0, 10, 0)
    attendance_percentage = st.number_input("Attendance Percentage", 0, 100, 85)
    # backlogs = st.number_input("Number of Backlogs", 0, 10, 0)
    extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"])

st.divider()

if st.button("Predict Placement Status", type = 'primary'):
    payload = {
        "gender": gender,
        "ssc_percentage": ssc_percentage,
        "hsc_percentage": hsc_percentage,
        "degree_percentage": degree_percentage,
        "cgpa": cgpa,
        "entrance_exam_score": entrance_exam_score,
        "technical_skill_score": technical_skill_score,
        "soft_skill_score": soft_skill_score,
        "internship_count": internship_count,
        "live_projects": live_projects,
        "work_experience_months": work_experience_months,
        "certifications": certifications,
        "attendance_percentage": attendance_percentage,
        # "backlogs": backlogs,
        "extracurricular_activities": extracurricular
    }

    with st.spinner("Menghubungi API Backend..."):
        try:
            response = requests.post(API_URL_BASE, json = payload)
            if response.status_code == 200:
                result = response.json()

                if result['status'] == 1:
                    st.success("Hasil Prediksi: TERSEDIA (PLACED)")
                    st.metric("\tPrediksi Gaji:", f"{result['salary']:,.2f} LPA")
                else:
                    st.warning("Hasil Prediksi: TIDAK TERSEDIA (NOT PLACED)")
            else:
                st.error(f"BACKEND ERROR: {response.status_code}")
        except Exception as e:
            st.error(f"Gagal Terhubung Ke Backend!")
