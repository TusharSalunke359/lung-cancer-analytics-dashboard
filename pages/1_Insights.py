import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 KPI Insights Dashboard")

# Load data
df = pd.read_csv("gold_data.csv")

# Sidebar filters (future-ready)
st.sidebar.header("🔍 Filters")
show_raw = st.sidebar.checkbox("Show Raw Data")

# =========================
# KPI SECTION
# =========================

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", int(df['total_patients'][0]))
col2.metric("High Risk Patients", int(df['high_risk_patients'][0]))
col3.metric("High Risk %", f"{df['high_risk_percentage'][0]:.2f}%")
col4.metric("Recovery Rate %", f"{df['recovery_rate_percentage'][0]:.2f}%")

col5, col6 = st.columns(2)

col5.metric("Avg Risk Score", round(df['avg_risk_score'][0], 2))
col6.metric("Avg Survival Years", round(df['avg_survival_years'][0], 2))

# =========================
# CHARTS
# =========================

st.subheader("📈 Visual Insights")

col7, col8 = st.columns(2)

# Bar chart
with col7:
    chart_data = pd.DataFrame({
        "Metric": ["High Risk %", "Recovery %", "Smoker %"],
        "Value": [
            df['high_risk_percentage'][0],
            df['recovery_rate_percentage'][0],
            df['smoker_percentage'][0]
        ]
    })
    st.bar_chart(chart_data.set_index("Metric"))

# Pie chart
with col8:
    pie_data = [
        df['high_risk_percentage'][0],
        100 - df['high_risk_percentage'][0]
    ]

    labels = ["High Risk", "Remaining"]

    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)

# =========================
# DATA TABLE
# =========================

if show_raw:
    st.subheader("📄 Data Snapshot")
    st.dataframe(df)

# =========================
# DOWNLOAD BUTTON
# =========================

st.download_button(
    label="📥 Download Data",
    data=df.to_csv(index=False),
    file_name="lung_kpi_data.csv",
    mime="text/csv"
)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption(f"Last Updated: {df['created_timestamp'][0]}")
st.caption("🚀 Built with Databricks + Streamlit")