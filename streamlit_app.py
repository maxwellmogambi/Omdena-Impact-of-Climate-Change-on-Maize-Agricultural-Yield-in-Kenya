#imports
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import os

# Initialize model
model = None

# Load the trained model
filename = os.path.join(os.path.dirname(__file__), 'ridge_regression_model.sav')

# Check if the file exists
if os.path.exists(filename):
    st.write(f"Model file found at {filename}.")
    try:
        with open(filename, 'rb') as model_file:
            model = pickle.load(model_file)
            st.success("Model loaded successfully!")
    except Exception as e:
        model = None
        st.error(f"Error loading the model: {str(e)}")
else:
    st.error("Model file not found. Check the file path!")

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

# Add an image for aesthetic appeal
# st.image("path_to_your_image.jpg", use_column_width=True)  # Replace with your image path



# Create a dictionary of input fields and their default values with min/max values
input_defaults = {
    'temperature_2m (°C)': (24.0, 26.0),  # Min, Max values
    'temperature_2m_max (°C)': (31.0, 33.0),  # Min, Max values
    'temperature_2m_min (°C)': (18.0, 20.0),  # Min, Max values
    'total_precipitation_sum (mm)': (409.0, 991.0),  # Min, Max values
    'u_component_of_wind_10m (m/s)': (-2.1, -1.3),  # Min, Max values
    'precipitation (mm)': (443.0, 971.0)  # Min, Max values
}

# Initialize session state using the dictionary
for key, (min_value, max_value) in input_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = min_value  # Default value set to min value

# Create 2 columns
col1, col2 = st.columns(2)

# Column 1 inputs with min and max values
with col1:
    st.session_state['temperature_2m (°C)'] = st.number_input(
        "Temperature 2m (°C)", 
        value=st.session_state['temperature_2m (°C)'], 
        min_value=input_defaults['temperature_2m (°C)'][0], 
        max_value=input_defaults['temperature_2m (°C)'][1]
    )
    st.session_state['temperature_2m_max (°C)'] = st.number_input(
        "Max Temperature 2m (°C)", 
        value=st.session_state['temperature_2m_max (°C)'], 
        min_value=input_defaults['temperature_2m_max (°C)'][0], 
        max_value=input_defaults['temperature_2m_max (°C)'][1]
    )
    st.session_state['temperature_2m_min (°C)'] = st.number_input(
        "Min Temperature 2m (°C)", 
        value=st.session_state['temperature_2m_min (°C)'], 
        min_value=input_defaults['temperature_2m_min (°C)'][0], 
        max_value=input_defaults['temperature_2m_min (°C)'][1]
    )

# Column 2 inputs with min and max values
with col2:
    st.session_state['total_precipitation_sum (mm)'] = st.number_input(
        "Total Precipitation (mm)", 
        value=st.session_state['total_precipitation_sum (mm)'], 
        min_value=input_defaults['total_precipitation_sum (mm)'][0], 
        max_value=input_defaults['total_precipitation_sum (mm)'][1]
    )
    st.session_state['u_component_of_wind_10m (m/s)'] = st.number_input(
        "U Component of Wind 10m (m/s)", 
        value=st.session_state['u_component_of_wind_10m (m/s)'], 
        min_value=input_defaults['u_component_of_wind_10m (m/s)'][0], 
        max_value=input_defaults['u_component_of_wind_10m (m/s)'][1]
    )
    st.session_state['precipitation (mm)'] = st.number_input(
        "Precipitation (mm)", 
        value=st.session_state['precipitation (mm)'], 
        min_value=input_defaults['precipitation (mm)'][0], 
        max_value=input_defaults['precipitation (mm)'][1]
    )

# Button to make predictions
if st.button("Predict Maize Yield"):
    input_data = [
        st.session_state['temperature_2m (°C)'], 
        st.session_state['temperature_2m_max (°C)'], 
        st.session_state['temperature_2m_min (°C)'], 
        st.session_state['total_precipitation_sum (mm)'], 
        st.session_state['u_component_of_wind_10m (m/s)'], 
        st.session_state['precipitation (mm)']
    ]

    # Log inputs for debugging (optional)
    st.write(f"Input data: {input_data}")
    
    # Call the predict function
    try:
        predicted_yield = predict_yield(input_data)
        st.success(f"Predicted Maize Yield: {predicted_yield:.2f} MT/HA")
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
