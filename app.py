from ast import main
import streamlit as st
import requests
import pandas as pd
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'srv1020.hstgr.io',
    'database': 'u830421930_sensor_databas',  # REPLACE with your Database name
    'user': 'u830421930_sensordatabas',      # REPLACE with Database user
    'password': '12sensData'   # REPLACE with Database user password
}

# Function to fetch sensor data
def fetch_sensor_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT id, sensor, location, distance, reading_time FROM sensordata ORDER BY id DESC LIMIT 7"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to fetch the latest sensor value
def fetch_latest_sensor_value():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT sensor FROM sensordata ORDER BY reading_time DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Streamlit application
st.set_page_config(page_title="Sensor Data", layout="wide")
st.title("SENSOR DATA")
st.write("*Note: When device is offline, no data will be updated.")

# Fetch and display sensor data
sensor_data = fetch_sensor_data()

# Rename columns as needed
sensor_data.columns = ['ID', 'Temprature', 'Humidity', 'Moisters', 'Reading Time']

# Display the table with updated headers
st.table(sensor_data)

# Check the latest sensor value
latest_sensor_value = fetch_latest_sensor_value()
threshold = 32  # Example threshold value

if latest_sensor_value is not None:
    try:
        latest_sensor_value = float(latest_sensor_value)
        st.write(f"Latest Sensor Value: {latest_sensor_value}")

        if latest_sensor_value > threshold:
            st.warning("Alert: Sensor value exceeds the threshold.")
        else:
            st.info("Sensor value is within normal range.")
    except ValueError:
        st.error("Latest sensor value is not a valid number.")
else:
    st.error("No sensor data found.")

# Visualize sensor data
st.header("Sensor Data Visualization")

# Fetch data for visualization
data = fetch_sensor_data()

if not data.empty:
    # Create columns for side-by-side display
    col1, col2 = st.columns(2)

    # Temperature Chart
    with col1:
        st.header("Temperature")
        if 'reading_time' in data.columns and 'sensor' in data.columns:
            st.subheader("Temperature Line Chart")
            st.line_chart(data[['reading_time', 'sensor']].set_index('reading_time'))
        else:
            st.warning("Data does not contain required columns for temperature charting.")

    # Humidity Chart
    with col2:
        st.header("Humidity")
        if 'reading_time' in data.columns and 'location' in data.columns:
            st.subheader("Humidity Line Chart")
            st.line_chart(data[['reading_time', 'location']].set_index('reading_time'))
        else:
            st.warning("Data does not contain required columns for humidity charting.")
else:
    st.write("No data available for visualization.")

# Tomato Information Generator
st.title("Framers Prompt to transform leading productivity ")

# Input for the user's question
q = st.text_input("Question")

# Button to submit the question
if st.button("Submit"):
    if q:
        # Define the API endpoint
        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

        # Prepare the request body
        body = {
            "input": f"""Answer the following question using only information from the article. If there is no good answer in the article, say "I don't know".

Article: 
###
Tomatoes are one of the most popular plants for vegetable gardens. Tip for success: If you select varieties that are resistant to disease and pests, growing tomatoes can be quite easy. For experienced gardeners looking for a challenge, there are endless heirloom and specialty varieties to cultivate. Tomato plants come in a range of sizes. There are varieties that stay very small, less than 12 inches, and grow well in a pot or hanging basket on a balcony or patio. Some grow into bushes that are a few feet high and wide, and can be grown in larger containers. Other varieties grow into huge bushes that are several feet wide and high in a planter or garden bed. Still other varieties grow as long vines, six feet or more, and love to climb trellises. Tomato plants do best in full sun. You need to water tomatoes deeply and often. Using mulch prevents soil-borne disease from splashing up onto the fruit when you water. Pruning suckers and even pinching the tips will encourage the plant to put all its energy into producing fruit.
###
Question: Is growing tomatoes easy?
Answer: Yes, if you select varieties that are resistant to disease and pests.

Question: What varieties of tomatoes are there?
Answer: There are endless heirloom and specialty varieties.
Question: {q}
Answer:""",
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 100,
                "stop_sequences": ["\n\n"],
                "repetition_penalty": 1
            },
            "model_id": "meta-llama/llama-3-8b-instruct",
            "project_id": "bc010f4d-391c-4c1b-98dc-a0e0e7e4216d"
        }

        # Define headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBKMEZGIiwiaWQiOiJJQk1pZC02OTQwMDBKMEZGIiwicmVhbG1pZCI6IklCTWlkIiwic2Vzc2lvbl9pZCI6IkMtOGIzYzQxNTYtNzI5ZC00NGU0LTkxN2MtM2ZjZjY5NTI5OTI0Iiwic2Vzc2lvbl9leHBfbWF4IjoxNzI3MDIzMzU4LCJzZXNzaW9uX2V4cF9uZXh0IjoxNzI2OTQ0MTc1LCJqdGkiOiI1ODY0NjVhMy1mZWZkLTQ4N2MtOWI0Mi00NDNiZGFkYTNhMGYiLCJpZGVudGlmaWVyIjoiNjk0MDAwSjBGRiIsImdpdmVuX25hbWUiOiJCYWxhZ2FqYXJhaiIsImZhbWlseV9uYW1lIjoiUHJhYmhha2FyIiwibmFtZSI6IkJhbGFnYWphcmFqIFByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSIsInN1YiI6ImJhbGFwcmFiaGE2MEBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJiYWxhcHJhYmhhNjBAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk0MDAwSjBGRiIsIm5hbWUiOiJCYWxhZ2FqYXJhaiBQcmFiaGFrYXIiLCJnaXZlbl9uYW1lIjoiQmFsYWdhamFyYWoiLCJmYW1pbHlfbmFtZSI6IlByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJjNjkzNTFiNGNjYjk0MmRlOTAzMzJkNWUzOTMyYWI3NCIsImltc191c2VyX2lkIjoiMTI2ODc5NTciLCJpbXMiOiIyNzUwMjIyIn0sImlhdCI6MTcyNjkzNjk3MiwiZXhwIjoxNzI2OTM4MTcyLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6cGFzc2NvZGUiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJieCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.LibqjNLq6z6OA2TYp2WD55OXxwREYFho20Zz4N6kmdWFFcM7x4Gb3WydZWU0FXqEJ1BSCrCsDqDmKxWIhHBrlBwlFhd_Ct5gOP5bJwH7PnLFQAqcAQeznQ5C4ybvK1HiDjyGb4ZwyK-UnebFxrYzgNHOXgm3eX84IYBYuYGGGorIMAPwR2d_HhEEeuaF1ViOOj6HHPWOE5JIq7lg96Fn0mPKIu9gaq22MrGT_6BpjONtlnc0wn-zrsxOlrtg5RiYcw2VDfuKb4wWowWNxON1eJCMlly6FsjJ6B8lk1KPKWlSDeOSG8vSnPfND3YVdMePc9DWAPHMfwxxqTVoBhTa3Q"
        }

        # Send the POST request
        response = requests.post(url, headers=headers, json=body)

        # Check for a successful response and display the result
        if response.status_code == 200:
            data = response.json()
            st.success(data["results"][0]['generated_text'])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a question.")
st.write("Recommendations to farmers enhance productivity")
if __name__ == "__main__":
    main()
