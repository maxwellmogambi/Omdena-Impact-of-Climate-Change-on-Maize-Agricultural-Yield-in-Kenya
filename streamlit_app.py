#imports
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import os

# Load the trained model
filename = os.path.join(os.path.dirname(__file__), 'Tuned_Ridge_Reg.sav')

# Check if the file exists
if os.path.exists(filename):
    st.write(f"Model file found at {filename}.")
else:
    st.error("Model file not found. Check the file path!")

try:
    with open(filename, 'rb') as model_file:
        model = pickle.load(model_file)
        st.success("Model loaded successfully!")
except Exception as e:
    model = None
    st.error(f"Error loading the model: {str(e)}")
    

# Define the function to make predictions
def predict_yield(input_data):
    if model is None:
        raise ValueError("Model not loaded properly.")
    input_data = np.array(input_data).reshape(1, -1)  # Reshape the input for prediction
    try:
        prediction = model.predict(input_data)
        return prediction[0]
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None

# Streamlit app interface
st.title("Maize Yield Prediction in Kenya")
st.write("Enter the climate parameters to predict maize yield:")

# Create a dictionary of input fields and their default values
input_defaults = {
    'soil_temp_L1_C': 0.0,
    'soil_temp_L2_C': 0.0,
    'soil_temp_L3_C': 0.0,
    'soil_temp_L4_C': 0.0,
    'temp_C': 0.0,
    'precipitation_era5_mm': 0.0,
    'precipitation_chirps_mm': 0.0,
    'area_harvested_usda_1000ha': 0.0,
    'area_harvested_fao_1000ha': 0.0,
    'wind_northward_m_s': 0.0,
    'soil_water_L2_fraction': 0.0,
    'soil_water_L4_fraction': 0.0,
    'production_usda_1000ha': 0.0,
    'production_fao_1000ha': 0.0
}

# Initialize session state using the dictionary
for key, default_value in input_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Column 1 inputs
with col1:
    st.session_state['soil_temp_L1_C'] = st.number_input("Soil Temperature L1 (C)", value=st.session_state['soil_temp_L1_C'])
    st.session_state['soil_temp_L2_C'] = st.number_input("Soil Temperature L2 (C)", value=st.session_state['soil_temp_L2_C'])
    st.session_state['soil_temp_L3_C'] = st.number_input("Soil Temperature L3 (C)", value=st.session_state['soil_temp_L3_C'])
    st.session_state['soil_temp_L4_C'] = st.number_input("Soil Temperature L4 (C)", value=st.session_state['soil_temp_L4_C'])


# Column 2 inputs
with col2:
    st.session_state['temp_C'] = st.number_input("Temperature (C)", value=st.session_state['temp_C'])
    st.session_state['precipitation_era5_mm'] = st.number_input("Precipitation (ERA5, mm)", value=st.session_state['precipitation_era5_mm'])
    st.session_state['precipitation_chirps_mm'] = st.number_input("Precipitation (CHIRPS, mm)", value=st.session_state['precipitation_chirps_mm'])
    st.session_state['area_harvested_usda_1000ha'] = st.number_input("Area harvested (USDA, 1000 ha)", value=st.session_state['area_harvested_usda_1000ha'])
    st.session_state['area_harvested_fao_1000ha'] = st.number_input("Area harvested (FAO, 1000 ha)", value=st.session_state['area_harvested_fao_1000ha'])


# Column 3 inputs
with col3:
    st.session_state['wind_northward_m_s'] = st.number_input("Wind Northward (m/s)", value=st.session_state['wind_northward_m_s'])
    st.session_state['soil_water_L2_fraction'] = st.number_input("Soil Water L2 Fraction", value=st.session_state['soil_water_L2_fraction'])
    st.session_state['soil_water_L4_fraction'] = st.number_input("Soil Water L4 Fraction", value=st.session_state['soil_water_L4_fraction'])
    st.session_state['production_usda_1000ha'] = st.number_input("Production (USDA, 1000 ha)", value=st.session_state['production_usda_1000ha'])
    st.session_state['production_fao_1000ha'] = st.number_input("Production (FAO, 1000 ha)", value=st.session_state['production_fao_1000ha'])

    
    
# Button to make predictions
if st.button("Predict Maize Yield"):
    input_data = [
        st.session_state['area_harvested_usda_1000ha'], st.session_state['production_usda_1000ha'], 
        st.session_state['area_harvested_fao_1000ha'], st.session_state['production_fao_1000ha'], 
        st.session_state['soil_temp_L1_C'], st.session_state['soil_temp_L2_C'], st.session_state['soil_temp_L3_C'], 
        st.session_state['soil_temp_L4_C'], st.session_state['temp_C'], st.session_state['precipitation_era5_mm'], 
        st.session_state['wind_northward_m_s'], st.session_state['soil_water_L2_fraction'], 
        st.session_state['soil_water_L4_fraction'], st.session_state['precipitation_chirps_mm']
    ]

    # Log inputs for debugging (optional)
    st.write(f"Input data: {input_data}")
    
    
    # Call the predict function
    try:
        predicted_yield = predict_yield(input_data)
        st.success(f"Predicted Maize Yield: {predicted_yield:.2f} tons/ha")
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
