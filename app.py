import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Lung Cancer App", layout="wide")

# =========================
# CUSTOM SIDEBAR STYLE
# =========================
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# =========================
# USER DATABASE (DUMMY)
# =========================
users = {
    "admin": "1234",
    "tushar": "pass123"
}

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN PAGE
# =========================
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

# =========================
# MAIN APP (AFTER LOGIN)
# =========================
def main_app():
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_Insights.py", label="📊 Insights")
        st.page_link("pages/2_Prediction.py", label="🤖 AI Prediction")

        st.markdown("---")

        st.markdown("## ⚙️ Controls")
        st.write("Medallion Architecture Project")

        st.markdown("---")

        st.markdown("## 👤 User")
        st.success("Logged in")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # ===== MAIN CONTENT =====
    st.title("🫁 Lung Cancer Analytics Dashboard")

    st.markdown("""
    ### 🚀 Project Overview

    This dashboard is built using:

    - **Bronze Layer** → Raw Data  
    - **Silver Layer** → Cleaned + SCD Type 2  
    - **Gold Layer** → KPI Aggregations  

    ### 📊 Features:
    - KPI Monitoring  
    - Risk Analysis  
    - AI Prediction  

    👉 Use the sidebar to navigate between pages
    """)

    st.success("✅ System is running successfully")

# =========================
# ROUTING
# =========================
if st.session_state.logged_in:
    main_app()
else:
    login()