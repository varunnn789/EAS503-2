import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

API_URL = "http://146.190.78.32:8080"

st.set_page_config(layout="wide")
st.title('Heart Disease Prediction App')

# Info button at the top
with st.expander("ℹ️ Variable Descriptions"):
    st.write("""
    - Height: Your height in meters
    - Weight: Your weight in kilograms
    - Physical Health Days: Number of days physical health was good in the past 30 days
    - Mental Health Days: Number of days mental health was good in the past 30 days
    - Sleep Hours: Average hours of sleep per 24-hour period
    - Sex: Biological sex
    - Age Category: Age group
    - Race/Ethnicity: Racial or ethnic background
    - General Health: Self-reported health status
    - Smoker Status: Current smoking habits
    - E-Cigarette Usage: Current or past e-cigarette use
    - Alcohol Drinker: Whether you consume alcohol
    - Had Diabetes: If you have been diagnosed with diabetes
    - Had Skin Cancer: If you have been diagnosed with skin cancer
    - Had Kidney Disease: If you have been diagnosed with kidney disease
    - High Risk Last Year: If you were told you're at high risk for heart disease or stroke in the past year
    """)

# Sidebar
st.sidebar.header('Input Parameters')

def randomize_inputs():
    return {
        'height': random.uniform(1.5, 2.0),
        'weight': random.uniform(50.0, 100.0),
        'physical_health_days': random.randint(0, 30),
        'mental_health_days': random.randint(0, 30),
        'sleep_hours': random.randint(4, 12),
        'sex': random.choice(['Male', 'Female']),
        'age_category': random.choice(['Age 18 to 24', 'Age 25 to 29', 'Age 30 to 34', 'Age 35 to 39', 'Age 40 to 44', 'Age 45 to 49', 'Age 50 to 54', 'Age 55 to 59', 'Age 60 to 64', 'Age 65 to 69', 'Age 70 to 74', 'Age 75 to 79', 'Age 80 or older']),
        'race_ethnicity': random.choice(['White only, Non-Hispanic', 'Black only, Non-Hispanic', 'Hispanic', 'Other']),
        'general_health': random.choice(['Excellent', 'Very good', 'Good', 'Fair', 'Poor']),
        'smoker_status': random.choice(['Current smoker - now smokes every day', 'Current smoker - now smokes some days', 'Former smoker', 'Never smoked']),
        'e_cigarette_usage': random.choice(['Never used e-cigarettes in my entire life', 'Use e-cigarettes every day', 'Use e-cigarettes some days', 'Former e-cigarette user']),
        'alcohol_drinkers': random.choice([True, False]),
        'had_diabetes': random.choice([True, False]),
        'had_skin_cancer': random.choice([True, False]),
        'had_kidney_disease': random.choice([True, False]),
        'high_risk_last_year': random.choice([True, False])
    }

if st.sidebar.button('Randomize Inputs'):
    st.session_state.random_inputs = randomize_inputs()

# Input fields
col1, col2 = st.sidebar.columns(2)

with col1:
    height = st.number_input('Height (m)', value=st.session_state.get('random_inputs', {}).get('height', 1.75), min_value=1.0, max_value=2.5, step=0.01, format="%.2f")
with col2:
    height_slider = st.slider('Height Slider', 1.0, 2.5, height, 0.01, format="%.2f")
height = height_slider

with col1:
    weight = st.number_input('Weight (kg)', value=st.session_state.get('random_inputs', {}).get('weight', 70.5), min_value=30.0, max_value=300.0, step=0.1, format="%.1f")
with col2:
    weight_slider = st.slider('Weight Slider', 30.0, 300.0, weight, 0.1, format="%.1f")
weight = weight_slider

with col1:
    physical_health_days = st.number_input('Physical Health Days', value=st.session_state.get('random_inputs', {}).get('physical_health_days', 28), min_value=0, max_value=30)
with col2:
    physical_health_days_slider = st.slider('Physical Health Days Slider', 0, 30, physical_health_days)
physical_health_days = physical_health_days_slider

with col1:
    mental_health_days = st.number_input('Mental Health Days', value=st.session_state.get('random_inputs', {}).get('mental_health_days', 29), min_value=0, max_value=30)
with col2:
    mental_health_days_slider = st.slider('Mental Health Days Slider', 0, 30, mental_health_days)
mental_health_days = mental_health_days_slider

with col1:
    sleep_hours = st.number_input('Sleep Hours', value=st.session_state.get('random_inputs', {}).get('sleep_hours', 7), min_value=0, max_value=24)
with col2:
    sleep_hours_slider = st.slider('Sleep Hours Slider', 0, 24, sleep_hours)
sleep_hours = sleep_hours_slider

sex = st.sidebar.selectbox('Sex', ['Male', 'Female'], index=['Male', 'Female'].index(st.session_state.get('random_inputs', {}).get('sex', 'Male')))
age_category = st.sidebar.selectbox('Age Category', ['Age 18 to 24', 'Age 25 to 29', 'Age 30 to 34', 'Age 35 to 39', 'Age 40 to 44', 'Age 45 to 49', 'Age 50 to 54', 'Age 55 to 59', 'Age 60 to 64', 'Age 65 to 69', 'Age 70 to 74', 'Age 75 to 79', 'Age 80 or older'], index=['Age 18 to 24', 'Age 25 to 29', 'Age 30 to 34', 'Age 35 to 39', 'Age 40 to 44', 'Age 45 to 49', 'Age 50 to 54', 'Age 55 to 59', 'Age 60 to 64', 'Age 65 to 69', 'Age 70 to 74', 'Age 75 to 79', 'Age 80 or older'].index(st.session_state.get('random_inputs', {}).get('age_category', 'Age 30 to 34')))
race_ethnicity = st.sidebar.selectbox('Race/Ethnicity', ['White only, Non-Hispanic', 'Black only, Non-Hispanic', 'Hispanic', 'Other'], index=['White only, Non-Hispanic', 'Black only, Non-Hispanic', 'Hispanic', 'Other'].index(st.session_state.get('random_inputs', {}).get('race_ethnicity', 'White only, Non-Hispanic')))
general_health = st.sidebar.selectbox('General Health', ['Excellent', 'Very good', 'Good', 'Fair', 'Poor'], index=['Excellent', 'Very good', 'Good', 'Fair', 'Poor'].index(st.session_state.get('random_inputs', {}).get('general_health', 'Very good')))
smoker_status = st.sidebar.selectbox('Smoker Status', ['Current smoker - now smokes every day', 'Current smoker - now smokes some days', 'Former smoker', 'Never smoked'], index=['Current smoker - now smokes every day', 'Current smoker - now smokes some days', 'Former smoker', 'Never smoked'].index(st.session_state.get('random_inputs', {}).get('smoker_status', 'Never smoked')))
e_cigarette_usage = st.sidebar.selectbox('E-Cigarette Usage', ['Never used e-cigarettes in my entire life', 'Use e-cigarettes every day', 'Use e-cigarettes some days', 'Former e-cigarette user'], index=['Never used e-cigarettes in my entire life', 'Use e-cigarettes every day', 'Use e-cigarettes some days', 'Former e-cigarette user'].index(st.session_state.get('random_inputs', {}).get('e_cigarette_usage', 'Never used e-cigarettes in my entire life')))

col3, col4 = st.sidebar.columns(2)
with col3:
    alcohol_drinkers = st.checkbox('Alcohol Drinker', value=st.session_state.get('random_inputs', {}).get('alcohol_drinkers', False))
    had_diabetes = st.checkbox('Had Diabetes', value=st.session_state.get('random_inputs', {}).get('had_diabetes', False))
    had_skin_cancer = st.checkbox('Had Skin Cancer', value=st.session_state.get('random_inputs', {}).get('had_skin_cancer', False))
with col4:
    had_kidney_disease = st.checkbox('Had Kidney Disease', value=st.session_state.get('random_inputs', {}).get('had_kidney_disease', False))
    high_risk_last_year = st.checkbox('High Risk Last Year', value=st.session_state.get('random_inputs', {}).get('high_risk_last_year', False))

# Make the predict button bigger and cover the entire row
if st.sidebar.button('Predict', use_container_width=True):
    # Calculate poor health days
    poor_physical_health_days = 30 - physical_health_days
    poor_mental_health_days = 30 - mental_health_days
    
    # Prepare the input data
    input_data = {
        "HeightInMeters": height,
        "WeightInKilograms": weight,
        "PhysicalHealthDays": poor_physical_health_days,
        "MentalHealthDays": poor_mental_health_days,
        "SleepHours": sleep_hours,
        "Sex": sex,
        "AgeCategory": age_category,
        "RaceEthnicityCategory": race_ethnicity,
        "GeneralHealth": general_health,
        "SmokerStatus": smoker_status,
        "ECigaretteUsage": e_cigarette_usage,
        "AlcoholDrinkers": alcohol_drinkers,
        "HadDiabetes": had_diabetes,
        "HadSkinCancer": had_skin_cancer,
        "HadKidneyDisease": had_kidney_disease,
        "HighRiskLastYear": high_risk_last_year
    }

    try:
        # Make prediction
        response = requests.post(f"{API_URL}/predict", json=input_data)
        result = response.json()

        # Display prediction
        st.subheader('Prediction Result')
        st.markdown(f"<h2 style='text-align: center; color: red;'>{result['Prediction']}</h2>", unsafe_allow_html=True)

        # Visualizations
        st.subheader('Health Insights')
        col1, col2 = st.columns(2)

        with col1:
            # BMI Calculation and Visualization
            bmi = weight / (height ** 2)
            bmi_category = pd.cut([bmi], bins=[0, 18.5, 25, 30, float('inf')], labels=['Underweight', 'Normal', 'Overweight', 'Obese'])[0]
            fig_bmi = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = bmi,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "BMI"},
                delta = {'reference': 25, 'position': "top"},
                gauge = {
                    'axis': {'range': [None, 40]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 18.5], 'color': "lightblue"},
                        {'range': [18.5, 25], 'color': "green"},
                        {'range': [25, 30], 'color': "yellow"},
                        {'range': [30, 40], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': bmi
                    }
                }
            ))
            st.plotly_chart(fig_bmi, key="bmi_chart")
            st.write(f"You seem to be in the {bmi_category} BMI Category")

            # BMI More than or Less than counter
            st.write("BMI is:")
            col1_1, col1_2, col1_3 = st.columns(3)
            with col1_1:
                st.metric("", f"{bmi:.1f}", f"{bmi - 25:.1f}")
            with col1_2:
                st.metric("Normal BMI", "25.0")

        with col2:
            # Sleep Hours Visualization
            fig_sleep = go.Figure(go.Indicator(
                mode = "number+gauge+delta",
                value = sleep_hours,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Sleep Hours"},
                delta = {'reference': 8, 'position': "top"},
                gauge = {
                    'axis': {'range': [0, 12]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 6], 'color': "red"},
                        {'range': [6, 7], 'color': "yellow"},
                        {'range': [7, 9], 'color': "green"},
                        {'range': [9, 12], 'color': "yellow"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': sleep_hours
                    }
                }
            ))
            st.plotly_chart(fig_sleep, key="sleep_chart")


        # Health Days Visualization
        health_data = pd.DataFrame({
            'Category': ['Good Physical Health', 'Poor Physical Health', 'Good Mental Health', 'Poor Mental Health'],
            'Days': [physical_health_days, poor_physical_health_days, mental_health_days, poor_mental_health_days]
        })
        fig_health = px.bar(health_data, x='Category', y='Days', color='Category', title='Physical and Mental Health Days in the Last Month')
        st.plotly_chart(fig_health, key="health_days_chart")


        # Risk Factors Visualization
        risk_factors = ['Alcohol Drinker', 'Diabetes', 'Skin Cancer', 'Kidney Disease', 'High Risk Last Year']
        risk_values = [alcohol_drinkers, had_diabetes, had_skin_cancer, had_kidney_disease, high_risk_last_year]
        # Create a list of tuples for selected risk factors only
        selected_risks = [(factor, 1) for factor, value in zip(risk_factors, risk_values) if value]
        if selected_risks:
            # Create DataFrame with only the selected risks
            risk_data = pd.DataFrame(selected_risks, columns=['Factor', 'Present'])
            
            # Create bar chart with custom colors and layout
            fig_risk = px.bar(
                risk_data, 
                x='Factor', 
                y='Present',
                title='Present Risk Factors',
                color='Factor',
                height=400
            )
            
            # Update layout to make it more readable
            fig_risk.update_layout(
                showlegend=True,
                yaxis_visible=False,
                yaxis_showticklabels=False
            )
            
            st.plotly_chart(fig_risk, key="risk_factors_chart")
        else:
            st.write("No risk factors selected.")


    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the prediction server: {str(e)}")

    st.sidebar.header('About')
    st.sidebar.info('This app predicts the likelihood of heart disease based on various health factors.')