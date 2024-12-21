import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('Heart Disease Prediction App')

# Input fields
height = st.number_input('Height (in meters)', value=1.75, min_value=1.0, max_value=2.5, step=0.01)
weight = st.number_input('Weight (in kilograms)', value=70.5, min_value=30.0, max_value=300.0, step=0.1)
physical_health_days = st.number_input('Number of days physical health not good (last 30 days)', value=2, min_value=0, max_value=30)
mental_health_days = st.number_input('Number of days mental health not good (last 30 days)', value=1, min_value=0, max_value=30)
sleep_hours = st.number_input('Average hours of sleep per day', value=7.5, min_value=0.0, max_value=24.0, step=0.1)

sex = st.selectbox('Sex', ['Female', 'Male'])

age_categories = [
    'Age 18 to 24', 'Age 25 to 29', 'Age 30 to 34', 'Age 35 to 39',
    'Age 40 to 44', 'Age 45 to 49', 'Age 50 to 54', 'Age 55 to 59',
    'Age 60 to 64', 'Age 65 to 69', 'Age 70 to 74', 'Age 75 to 79',
    'Age 80 or older'
]
age_category = st.selectbox('Age Category', age_categories, index=2)

race_ethnicity = st.selectbox('Race/Ethnicity', ['White only, Non-Hispanic', 'Black only, Non-Hispanic', 'Hispanic', 'Other'])

general_health_categories = ['Poor', 'Fair', 'Good', 'Very good', 'Excellent']
general_health = st.selectbox('General Health', general_health_categories, index=3)

smoker_status_categories = [
    'Never smoked',
    'Former smoker',
    'Current smoker - now smokes some days',
    'Current smoker - now smokes every day'
]
smoker_status = st.selectbox('Smoker Status', smoker_status_categories, index=0)

e_cigarette_usage_categories = [
    'Never used e-cigarettes in my entire life',
    'Former e-cigarette user',
    'Use e-cigarettes some days',
    'Use e-cigarettes every day'
]
e_cigarette_usage = st.selectbox('E-Cigarette Usage', e_cigarette_usage_categories, index=0)

alcohol_drinkers = st.checkbox('Alcohol Drinker', value=False)
had_diabetes = st.checkbox('Had Diabetes', value=False)
had_skin_cancer = st.checkbox('Had Skin Cancer', value=False)
had_kidney_disease = st.checkbox('Had Kidney Disease', value=False)
high_risk_last_year = st.checkbox('High Risk Last Year', value=False)

if st.button('Predict'):
    # Prepare the input data
    input_data = {
        "HeightInMeters": height,
        "WeightInKilograms": weight,
        "PhysicalHealthDays": physical_health_days,
        "MentalHealthDays": mental_health_days,
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

    # Make prediction
    response = requests.post("http://localhost:8000/predict", json=input_data)
    result = response.json()

    # Display prediction
    st.subheader('Prediction Result')
    st.write(result['Prediction'])

    # Visualizations
    st.subheader('Health Insights')

    # BMI Calculation and Visualization
    bmi = weight / (height ** 2)
    bmi_category = pd.cut([bmi], bins=[0, 18.5, 25, 30, float('inf')], labels=['Underweight', 'Normal', 'Overweight', 'Obese'])[0]

    fig_bmi = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "BMI"},
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
    st.plotly_chart(fig_bmi)
    st.write(f"BMI Category: {bmi_category}")

    # Health Days Visualization
    health_data = pd.DataFrame({
        'Category': ['Good Physical Health', 'Poor Physical Health', 'Good Mental Health', 'Poor Mental Health'],
        'Days': [30 - physical_health_days, physical_health_days, 30 - mental_health_days, mental_health_days]
    })
    fig_health = px.bar(health_data, x='Category', y='Days', color='Category',
                        title='Physical and Mental Health Days in the Last Month')
    st.plotly_chart(fig_health)

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
    st.plotly_chart(fig_sleep)

    # Risk Factors Visualization
    risk_factors = ['Alcohol Drinker', 'Diabetes', 'Skin Cancer', 'Kidney Disease', 'High Risk Last Year']
    risk_values = [alcohol_drinkers, had_diabetes, had_skin_cancer, had_kidney_disease, high_risk_last_year]
    risk_data = pd.DataFrame({'Factor': risk_factors, 'Present': risk_values})
    fig_risk = px.bar(risk_data, x='Factor', y='Present', color='Present',
                      title='Presence of Risk Factors')
    st.plotly_chart(fig_risk)

st.sidebar.header('About')
st.sidebar.info('This app predicts the likelihood of heart disease based on various health factors.')
