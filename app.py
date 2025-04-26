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

# Define the feature types and default values
feature_inputs = {
    'age': ('number', 18, 100, 30),
    'MonthlyIncome': ('number', 0, 100000, 5000),
    'DebtRatio': ('slider', 0.0, 5.0, 0.01, 0.5),
    'RevolvingUtilizationOfUnsecuredLines': ('slider', 0.0, 2.0, 0.01, 0.5),
    'NumberOfOpenCreditLinesAndLoans': ('number', 0, 50, 5),
    'NumberOfDependents': ('number', 0, 10, 0),
    'NumberOfTimes90DaysLate': ('number', 0, 10, 0),
    'NumberOfTime30-59DaysPastDueNotWorse': ('number', 0, 10, 0),
    'NumberRealEstateLoansOrLines': ('number', 0, 10, 0),
    'NumberOfTime60-89DaysPastDueNotWorse': ('number', 0, 10, 0),
}

# Input Section
st.markdown("## 📋 Customer Information")

input_data = {}
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]
i = 0

for feature in feature_inputs:
    input_type = feature_inputs[feature][0]
    if input_type == 'number':
        min_val, max_val, default = feature_inputs[feature][1], feature_inputs[feature][2], feature_inputs[feature][3]
        input_data[feature] = columns[i % 3].number_input(f'{feature}', min_value=min_val, max_value=max_val, value=default)
    elif input_type == 'slider':
        min_val, max_val, step, default = feature_inputs[feature][1], feature_inputs[feature][2], feature_inputs[feature][3], feature_inputs[feature][4]
        input_data[feature] = columns[i % 3].slider(f'{feature}', min_val, max_val, value=default, step=step)
    i += 1

# Predict Button
st.markdown("### ")
if st.button('🔮 Predict Risk'):

    with st.spinner('Predicting... Hold tight ⏳'):
        # Add 'Unnamed: 0' column
        input_data['Unnamed: 0'] = 0

        # Create DataFrame
        input_df = pd.DataFrame([input_data])

        # Reorder columns according to model
        input_df = input_df[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(input_df)
        proba = model.predict_proba(input_df)

        # Small delay for effect
        time.sleep(1)

    # Results Layout
    st.markdown("---")
    st.markdown("## 📊 Prediction Result")

    risk_percentage = proba[0][1] * 100
    safe_percentage = proba[0][0] * 100

    if prediction[0] == 1:
        st.error("🚨 **High Financial Risk Detected!**")
    else:
        st.success("✅ **Low Financial Risk Detected!**")

    # Show risk probability as progress bar
    st.markdown("#### Risk Probability")
    st.progress(risk_percentage/100)

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
            {''.join([f"<li><b>{key}:</b> {value}</li>" for key, value in input_data.items() if key != 'Unnamed: 0'])}
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
