import streamlit as st
import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from streamlit_option_menu import option_menu

# Load dataset
data = pd.read_csv('Crop_Recommendation1.csv')

# Prepare data
X = data.drop(['label'], axis=1)
Y = data[['label']]
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier(random_state=42)
model.fit(xtrain, ytrain)

# History storage
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Crop Recommendation System",
        options=["Predict Crop", "Prediction History", "Crop Info", "About"],
        icons=["leaf", "clock-history", "info-square", "question-circle"],
        menu_icon="bar-chart",
        default_index=0
    )

# ========== TAB 1: Predict Crop ==========
if selected == "Predict Crop":
    st.title("🌱 Crop Recommendation System")
    st.markdown("Enter the soil and environmental parameters below:")

    ph = st.number_input("pH", min_value=0.0, max_value=14.0, format="%.2f")
    moisture = st.number_input("Moisture", min_value=0.0, format="%.2f")
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, format="%.2f")
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, format="%.2f")
    npk = st.number_input("NPK Value", min_value=0.0, format="%.2f")

    st.markdown(f"**Current Date & Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if st.button("Predict Crop"):
        try:
            input_data = np.array([[ph, moisture, temperature, humidity, npk]])
            prediction = model.predict(input_data)[0]
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.prediction_history.append((timestamp, prediction, ph, moisture, temperature, humidity, npk))
            st.success(f"🌾 Recommended Crop: **{prediction}**")
        except:
            st.error("Invalid input. Please enter numerical values.")

# ========== TAB 2: History ==========
elif selected == "Prediction History":
    st.title("📜 Prediction History")
    if st.session_state.prediction_history:
        df = pd.DataFrame(st.session_state.prediction_history,
                          columns=["Time", "Crop", "pH", "Moisture", "Temperature", "Humidity", "NPK"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No prediction history available.")

# ========== TAB 3: Crop Info ==========
elif selected == "Crop Info":
    st.title("🌾 Crop Information Table")
    crop_info = {
        'rice': [5.5, 7.5, 20, 35, 60, 90, 50],
        'wheat': [6.0, 7.0, 15, 25, 50, 80, 40],
        'maize': [5.8, 7.2, 18, 32, 40, 70, 60],
        'cotton': [6.0, 8.0, 25, 35, 40, 60, 45],
        'sugarcane': [6.2, 7.8, 22, 30, 70, 85, 65]
    }

    rows = []
    for crop, vals in crop_info.items():
        rows.append({
            'Crop': crop,
            'pH Range': f"{vals[0]}–{vals[1]}",
            'Moisture': f"{vals[2]}–{vals[3]}",
            'Temperature': f"{vals[4]}–{vals[5]} °C",
            'Humidity': f"{vals[6]}–90 %",
            'NPK (est.)': 'Varies'
        })

    st.dataframe(pd.DataFrame(rows))

# ========== TAB 4: About ==========
elif selected == "About":
    st.title("ℹ️ About This Tool")
    st.markdown("""
    This tool is designed to empower **small landowner farmers**  
    by providing **real-time crop recommendations** based on soil health.

    **Inputs considered:**
    - pH
    - Moisture
    - Temperature
    - Humidity
    - NPK (Nutrient) Levels

    **Developed using:**
    - Python
    - Streamlit (Web UI)
    - Decision Tree Classifier (Machine Learning)

    
    """)
