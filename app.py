import streamlit as st
import pandas as pd
import joblib
import time

# Load your trained model
model = joblib.load('model.pkl')

# Set page config
st.set_page_config(page_title="Financial Risk Assessment", page_icon="💰", layout="wide")

# App Title
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>💰 Financial Risk Assessment Dashboard</h1>
    <h4 style='text-align: center; color: gray;'>Predict financial risk instantly with AI</h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# Input Section - Use cards and hover effect
st.markdown("## 📋 Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.3s;">
        <h4>🎂 Age</h4>
        """,
        unsafe_allow_html=True
    )
    age = st.number_input('Age', min_value=18, max_value=100, value=30)
    st.markdown("</div>", unsafe_allow_html=True)  # Close the card

with col2:
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.3s;">
        <h4>💵 Monthly Income</h4>
        """,
        unsafe_allow_html=True
    )
    monthly_income = st.number_input('Monthly Income (INR)', min_value=0, value=5000)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.3s;">
        <h4>💳 Debt Ratio</h4>
        """,
        unsafe_allow_html=True
    )
    debt_ratio = st.slider('Debt Ratio (%)', 0.0, 5.0, step=0.01)
    st.markdown("</div>", unsafe_allow_html=True)

# Add more columns for the other inputs similarly with cards

# Predict Button
st.markdown("### ")
if st.button('🔮 Predict Risk'):

    with st.spinner('Predicting... Hold tight ⏳'):
        # Create input data
        input_data = pd.DataFrame({
            'age': [age],
            'MonthlyIncome': [monthly_income],
            'DebtRatio': [debt_ratio],
            'RevolvingUtilizationOfUnsecuredLines': [revolving_utilization],
            'NumberOfOpenCreditLinesAndLoans': [open_credit_lines],
            'NumberOfDependents': [num_dependents],
            'NumberOfTimes90DaysLate': [times_90_days_late],
            'NumberOfTime30-59DaysPastDueNotWorse': [num_30_59_days_past_due],
            'NumberRealEstateLoansOrLines': [real_estate_loans],
            'NumberOfTime60-89DaysPastDueNotWorse': [num_60_89_days_past_due]
        })

        # Add Unnamed:0 column
        input_data['Unnamed: 0'] = 0

        # Reorder columns to match model
        input_data = input_data[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(input_data)
        proba = model.predict_proba(input_data)

        # Small delay for effect
        time.sleep(1)

    # Results Layout
    st.markdown("---")
    st.markdown("## 📊 Prediction Result")

    risk_percentage = proba[0][1] * 100
    safe_percentage = proba[0][0] * 100

    # Convert result to INR
    risk_percentage_inr = risk_percentage * 75  # Assuming 1 USD = 75 INR for display
    safe_percentage_inr = safe_percentage * 75

    if prediction[0] == 1:
        st.error("🚨 **High Financial Risk Detected!**")
    else:
        st.success("✅ **Low Financial Risk Detected!**")

    # Show risk probability as progress bar
    st.markdown("#### Risk Probability")
    st.progress(risk_percentage / 100)

    st.markdown(f"**Risk Probability:** `{risk_percentage_inr:.2f} INR`")
    st.markdown(f"**Safe Probability:** `{safe_percentage_inr:.2f} INR`")

    st.markdown("---")
    st.info("⚡ *Note: Higher risk probability indicates increased chances of financial delinquency.*")

    # Customer Profile Summary
    st.markdown("## 🧾 Customer Profile Summary")

    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
        <ul>
            <li><b>Age:</b> {age}</li>
            <li><b>Monthly Income:</b> ₹{monthly_income}</li>
            <li><b>Debt Ratio:</b> {debt_ratio}</li>
            <li><b>Revolving Utilization:</b> {revolving_utilization}</li>
            <li><b>Open Credit Lines:</b> {open_credit_lines}</li>
            <li><b>Times 90 Days Late:</b> {times_90_days_late}</li>
            <li><b>Times 30-59 Days Past Due:</b> {num_30_59_days_past_due}</li>
            <li><b>Real Estate Loans/Lines:</b> {real_estate_loans}</li>
            <li><b>Times 60-89 Days Past Due:</b> {num_60_89_days_past_due}</li>
            <li><b>Dependents:</b> {num_dependents}</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    """
    <br><br>
    <hr style="border:1px solid #eee"/>
    <center style="color:gray;">
    Made with ❤️ by [Yashmit] | Powered by Yash & co. 🚀
    </center>
    """,
    unsafe_allow_html=True
)
