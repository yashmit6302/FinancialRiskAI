import streamlit as st
import pandas as pd
import joblib
import time
import random

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
    # Age Input with icon and cool focus effect
    age = st.slider('🎂 **Age**', min_value=18, max_value=100, value=30, step=1, help="Select the age of the customer")
    num_dependents = st.number_input('👨‍👩‍👧‍👦 **Number of Dependents**', min_value=0, value=0, step=1, help="Enter the number of dependents")
    times_90_days_late = st.number_input('🕑 **Times 90 Days Late**', min_value=0, value=0, step=1, help="Enter the number of times the person was 90 days late")

with col2:
    monthly_income = st.number_input('💵 **Monthly Income ($)**', min_value=0, value=5000, step=500, help="Enter the customer's monthly income")
    debt_ratio = st.slider('💳 **Debt Ratio (%)**', 0.0, 5.0, value=2.0, step=0.01, help="Adjust the Debt Ratio")
    revolving_utilization = st.slider('📈 **Revolving Utilization (%)**', 0.0, 2.0, value=0.5, step=0.01, help="Adjust Revolving Utilization")

with col3:
    open_credit_lines = st.number_input('🏦 **Number of Open Credit Lines**', min_value=0, value=5, step=1, help="Enter the number of open credit lines")
    num_30_59_days_past_due = st.number_input('📅 **Number of Times 30-59 Days Past Due**', min_value=0, value=0, step=1, help="Enter the number of times 30-59 days late")
    real_estate_loans = st.number_input('🏠 **Number of Real Estate Loans or Lines**', min_value=0, value=0, step=1, help="Enter the number of real estate loans")
    num_60_89_days_past_due = st.number_input('📅 **Number of Times 60-89 Days Past Due**', min_value=0, value=0, step=1, help="Enter the number of times 60-89 days late")

# Custom CSS for hover effects and animation
st.markdown(
    """
    <style>
        .stSlider>div>div>input {
            background-color: #eaf5e0;
            border-radius: 15px;
            transition: transform 0.3s ease;
        }
        .stSlider>div>div>input:focus {
            transform: scale(1.05);
            box-shadow: 0 0 10px #4CAF50;
        }

        .stNumberInput>div>div>input {
            background-color: #eaf5e0;
            border-radius: 15px;
            transition: transform 0.3s ease;
        }
        .stNumberInput>div>div>input:focus {
            transform: scale(1.05);
            box-shadow: 0 0 10px #4CAF50;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.1);
        }

        .stNumberInput>div>div>input:focus {
            border: 2px solid #4CAF50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Predict Button
st.markdown("### ")
if st.button('🔮 **Predict Risk**'):

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

    # Decide color based on risk percentage
    if risk_percentage <= 20:
        risk_status = "🟢 **Very Low Financial Risk!**"
        bar_color = "green"
        st.balloons()  # Confetti animation for low risk!
    elif risk_percentage <= 40:
        risk_status = "🟡 **Low Financial Risk.**"
        bar_color = "yellow"
    elif risk_percentage <= 60:
        risk_status = "🟠 **Moderate Financial Risk.**"
        bar_color = "orange"
    elif risk_percentage <= 80:
        risk_status = "🔴 **High Financial Risk!**"
        bar_color = "red"
    else:
        risk_status = "🔥 **Very High Financial Risk (Critical)!**"
        bar_color = "darkred"

    # Show risk status and animate progress bar
    st.markdown(risk_status)
    st.markdown("#### Risk Probability")

    # Animation: fill progress bar step by step
    progress_placeholder = st.empty()
    progress_bar = 0
    while progress_bar < risk_percentage:
        progress_bar += random.randint(1, 3)  # Randomize the speed of progress to make it more dynamic
        if progress_bar > risk_percentage:
            progress_bar = risk_percentage
        progress_placeholder.markdown(
            f"""
            <div style="background-color: lightgray; border-radius: 10px; height: 25px;">
                <div style="background-color: {bar_color}; width: {progress_bar}%; height: 100%; border-radius: 10px; text-align: center; color: white;">
                    <b>{progress_bar:.2f}%</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.02)  # controls speed of animation

    st.markdown(f"**Risk Probability:** `{risk_percentage:.2f}%`")
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
    Made with ❤️ by Deepansh 
    </center>
    """,
    unsafe_allow_html=True
)
