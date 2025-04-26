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

# Input Section
st.markdown("## 📋 Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input('🎂 Age', min_value=18, max_value=100, value=30)
    num_dependents = st.number_input('👨‍👩‍👧‍👦 Number of Dependents', min_value=0, value=0)

with col2:
    monthly_income = st.number_input('💵 Monthly Income ($)', min_value=0, value=5000)
    debt_ratio = st.slider('💳 Debt Ratio (%)', 0.0, 5.0, step=0.01)

with col3:
    revolving_utilization = st.slider('📈 Revolving Utilization (%)', 0.0, 2.0, step=0.01)
    open_credit_lines = st.number_input('🏦 Number of Open Credit Lines', min_value=0, value=5)
    times_90_days_late = st.number_input('🕑 Times 90 Days Late', min_value=0, value=0)

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
            'NumberOfTimes90DaysLate': [times_90_days_late],
            'NumberOfDependents': [num_dependents]
        })

        # Add missing columns required by model and fill with 0
        input_data['NumberOfTime30-59DaysPastDueNotWorse'] = 0
        input_data['NumberRealEstateLoansOrLines'] = 0
        input_data['NumberOfTime60-89DaysPastDueNotWorse'] = 0

        # Reorder columns according to model
        input_data = input_data[[
            'RevolvingUtilizationOfUnsecuredLines',
            'age',
            'NumberOfTime30-59DaysPastDueNotWorse',
            'DebtRatio',
            'MonthlyIncome',
            'NumberOfOpenCreditLinesAndLoans',
            'NumberOfTimes90DaysLate',
            'NumberRealEstateLoansOrLines',
            'NumberOfTime60-89DaysPastDueNotWorse',
            'NumberOfDependents'
        ]]

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

    # Set Risk Levels and Color
    if risk_percentage <= 20:
        risk_status = "🟢 **Very Low Financial Risk!**"
        bar_color = "green"
    elif risk_percentage <= 40:
        risk_status = "🟡 **Low Financial Risk.**"
        bar_color = "yellow"
    elif risk_percentage <= 60:
        risk_status = "🟠 **Moderate Financial Risk.**"
        bar_color = "orange"
    elif risk_percentage <= 80:
        risk_status = "🛑 **High Financial Risk!**"
        bar_color = "red"
    else:
        risk_status = "🔥 **Very High Financial Risk (Critical)!**"
        bar_color = "darkred"

    # Show the status
    st.markdown(risk_status)

    # Show colored progress bar
    st.markdown("#### Risk Probability")
    st.markdown(
        f"""
        <div style="background-color: lightgray; border-radius: 10px; height: 25px;">
            <div style="background-color: {bar_color}; width: {risk_percentage}%; height: 100%; border-radius: 10px; text-align: center; color: white;">
                <b>{risk_percentage:.2f}%</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"**Safe Probability:** `{safe_percentage:.2f}%`")

    st.markdown("---")
    st.info("⚡ *Note: Higher risk probability indicates increased chances of financial delinquency.*")

    # Customer Profile Summary
    st.markdown("## 🧾 Customer Profile Summary")

    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
        <ul>
            <li><b>Age:</b> {age}</li>
            <li><b>Monthly Income:</b> ${monthly_income}</li>
            <li><b>Debt Ratio:</b> {debt_ratio}</li>
            <li><b>Revolving Utilization:</b> {revolving_utilization}</li>
            <li><b>Open Credit Lines:</b> {open_credit_lines}</li>
            <li><b>Times 90 Days Late:</b> {times_90_days_late}</li>
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
