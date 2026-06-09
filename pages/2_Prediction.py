import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import shap
import pandas as pd

st.title("🤖 Cancer Risk Prediction")

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.subheader("Enter Patient Details")

# =========================
# INPUTS
# =========================

age = st.slider("Age", 1, 100, 30)
smoking = st.selectbox("Smoking", ["No", "Yes"])

smoking_val = 1 if smoking == "Yes" else 0

# =========================
# PREDICTION BUTTON
# =========================

if st.button("Predict"):
    input_data = np.array([[age, smoking_val]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    risk_prob = probability[0][1]

    # =========================
    # SMART AI LOGIC
    # =========================

    if risk_prob > 0.75:
        st.error("🔴 HIGH RISK (Strong Confidence)")
        st.write("⚠️ Immediate medical attention recommended.")

    elif risk_prob > 0.50:
        st.warning("🟠 MEDIUM RISK")
        st.write("🧪 Further tests and monitoring advised.")

    else:
        st.success("🟢 LOW RISK")
        st.write("✅ Maintain a healthy lifestyle.")

    # =========================
    # CONFIDENCE
    # =========================

    st.progress(float(risk_prob))
    st.info(f"Confidence Level: {risk_prob * 100:.2f}%")

    # =========================
    # AI EXPLANATION
    # =========================

    st.markdown("### 🧠 AI Explanation")

    if smoking_val == 1:
        st.write("- Smoking increases lung cancer risk significantly.")

    if age > 50:
        st.write("- Higher age is associated with increased risk.")
    else:
        st.write("- Lower age reduces risk probability.")

    # =========================
    # SHAP EXPLAINABILITY 🔥 (FINAL FIXED)
    # =========================

    st.markdown("### 🧠 AI Explainability (SHAP)")

    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_data)

        # Handle SHAP output safely
        if isinstance(shap_values, list):
            shap_array = shap_values[-1][0]
        else:
            shap_array = shap_values[0]

        st.write("### Feature Contribution:")

        shap_df = pd.DataFrame({
            "Feature": ["Age", "Smoking"],
            "Impact": shap_array
        })

        fig, ax = plt.subplots()
        ax.barh(shap_df["Feature"], shap_df["Impact"], color="orange")

        ax.set_title("SHAP Contribution")
        ax.set_xlabel("Impact on Prediction")

        st.pyplot(fig)

    except Exception as e:
        st.warning("SHAP visualization not supported, fallback used.")

        for i, feature in enumerate(["Age", "Smoking"]):
            value = shap_array[i]

            # Convert safely to float
            if isinstance(value, (list, np.ndarray)):
                value = float(value[0])

            value = float(value)

            st.write(f"{feature}: {value:.4f}")

# =========================
# FEATURE IMPORTANCE 🔥
# =========================

st.markdown("### 📊 Feature Importance")

importances = model.feature_importances_
features = ["Age", "Smoking"]

fig, ax = plt.subplots()
ax.barh(features, importances, color="skyblue")

ax.set_title("Feature Importance")
ax.set_xlabel("Impact on Prediction")

st.pyplot(fig)