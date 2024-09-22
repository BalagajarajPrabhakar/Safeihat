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
st.title("Safeihat")
st.subheader("Empowering Farmers with Real-Time Data and AI: Enhancing Precision Agriculture through IBM Watsonx.ai and Generative Technology")

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
            "input": f"""Answer the following question using only information from the table. If there is no good answer in the table, say \"I don'\''t know\" do not generate answer from internet.

Article: 
###
ph	Moisture%	temperature°F	humidity%	npk	crop
1	100	20	30	1	rice
2	101	21	31	2	rice
3	102	22	32	3	rice
4	103	23	33	4	rice
5	104	24	34	5	rice
6	105	25	35	6	rice
7	106	26	36	7	rice
2	107	27	37	8	rice
2	108	28	38	9	rice
3	109	29	39	10	rice
4	110	30	40	11	rice
5	111	31	41	12	rice
6	112	32	42	13	rice
7	113	33	43	14	rice
2	114	34	44	15	rice
3	115	35	45	16	rice
4	116	36	46	17	rice
5	117	37	47	18	rice
6	118	38	48	19	rice
4	119	39	49	20	rice
5	120	40	50	21	rice
6	121	41	51	22	rice
7	122	42	52	23	rice
2	123	43	53	24	rice
3	124	44	54	25	rice
4	125	45	55	26	rice
2	126	46	56	27	rice
3	127	47	57	28	rice
4	128	48	58	29	rice
5	129	49	59	30	rice
6	130	50	60	31	rice
4	131	51	61	32	rice
5	132	52	62	33	rice
6	133	53	63	34	rice
7	134	54	64	35	rice
2	135	55	65	36	rice
3	136	56	66	37	rice
4	137	57	67	38	rice
2	138	58	68	39	rice
3	139	59	69	40	rice
4	140	60	70	41	rice
5	141	61	71	42	rice
6	142	62	72	43	rice
7	143	63	73	44	rice
2	144	64	74	45	rice
3	145	65	75	46	rice
4	146	66	76	47	rice
5	147	67	77	48	rice
6	148	68	78	49	rice
4	149	25	35	11	maize
5	150	26	36	12	maize
6	151	27	37	13	maize
7	152	28	38	14	maize
2	153	29	39	15	maize
3	154	30	40	16	maize
4	155	31	41	17	maize
3	156	32	42	18	maize
4	157	33	43	19	maize
2	158	34	44	20	maize
3	159	35	45	21	maize
4	160	36	46	22	maize
5	161	37	47	23	maize
6	162	38	48	24	maize
7	163	39	49	25	maize
2	164	40	50	26	maize
3	165	41	51	27	maize
4	166	42	52	28	maize
5	167	43	53	29	maize
6	168	44	54	30	maize
4	169	45	55	31	maize
5	170	46	56	32	maize
6	171	47	57	33	maize
7	172	48	58	34	maize
1	173	49	59	35	maize
2	174	50	60	36	maize
3	175	51	61	37	maize
4	176	52	62	38	maize
5	177	53	63	39	maize
6	178	54	64	40	maize
7	179	55	65	41	maize
2	180	56	66	42	maize
2	181	57	67	43	maize
3	182	58	68	44	maize
4	183	59	69	45	maize
5	184	60	70	46	maize
6	185	61	71	47	maize
7	186	62	72	48	maize
2	187	63	73	49	maize
3	188	64	74	50	maize
4	189	65	75	51	maize
5	190	66	76	52	maize
6	191	67	77	53	maize
4	192	68	78	54	maize
5	193	69	79	55	maize
6	194	70	80	56	maize
7	195	71	81	57	maize
2	196	72	82	58	maize
3	197	73	83	59	maize
4	198	74	84	60	maize
2	199	75	85	61	maize
3	100	20	32	32	chickpea
4	101	21	33	33	chickpea
5	102	22	34	34	chickpea
6	103	23	35	35	chickpea
4	104	24	36	36	chickpea
5	105	25	37	37	chickpea
6	106	26	38	38	chickpea
7	107	27	39	39	chickpea
2	108	28	40	40	chickpea
3	109	29	41	41	chickpea
4	110	30	42	42	chickpea
2	111	31	43	43	chickpea
3	112	32	44	44	chickpea
4	113	33	45	45	chickpea
5	114	34	46	46	chickpea
6	115	35	47	47	chickpea
7	116	36	48	48	chickpea
2	117	37	49	49	chickpea
3	118	38	50	50	chickpea
4	119	39	51	51	chickpea
5	120	40	52	52	chickpea
6	121	41	53	53	chickpea
4	122	42	54	54	chickpea
5	123	43	55	55	chickpea
6	124	44	56	56	chickpea
7	125	45	57	57	chickpea
2	126	46	58	58	chickpea
3	127	47	59	59	chickpea
4	128	48	60	60	chickpea
3	129	49	61	61	chickpea
4	130	50	62	62	chickpea
2	131	51	63	63	chickpea
3	132	52	64	64	chickpea
4	133	53	65	65	chickpea
5	134	54	66	66	chickpea
6	135	55	67	67	chickpea
7	136	56	68	68	chickpea
2	137	57	69	69	chickpea
3	138	58	70	70	chickpea
4	139	59	71	71	chickpea
5	140	60	72	72	chickpea
6	141	61	73	73	chickpea
4	142	62	74	74	chickpea
5	143	63	75	75	chickpea
6	144	64	76	76	chickpea
7	145	65	77	77	chickpea
1	146	66	78	78	chickpea
2	147	67	79	79	chickpea
3	148	68	80	80	chickpea
4	149	69	81	81	chickpea
5	150	70	82	82	chickpea
6	120	21	37	12	kidneybeans
7	121	50	38	13	kidneybeans
2	122	51	39	14	kidneybeans
2	123	52	40	15	kidneybeans
3	124	53	41	16	kidneybeans
4	125	54	42	17	kidneybeans
5	126	55	43	18	kidneybeans
6	127	56	44	19	kidneybeans
7	128	57	45	20	kidneybeans
2	129	58	46	21	kidneybeans
3	130	59	47	22	kidneybeans
4	131	60	48	23	kidneybeans
5	132	61	49	24	kidneybeans
6	133	62	50	25	kidneybeans
4	134	63	51	26	kidneybeans
5	135	64	52	27	kidneybeans
6	136	65	53	28	kidneybeans
7	137	66	54	29	kidneybeans
2	138	67	55	30	kidneybeans
3	139	68	56	31	kidneybeans
4	140	69	57	32	kidneybeans
2	141	70	58	33	kidneybeans
3	142	71	59	34	kidneybeans
4	143	72	60	35	kidneybeans
5	144	73	61	36	kidneybeans
6	145	74	62	37	kidneybeans
4	146	75	63	38	kidneybeans
5	147	76	64	39	kidneybeans
6	148	77	65	40	kidneybeans
7	149	78	66	41	kidneybeans
2	150	79	67	42	kidneybeans
3	151	80	68	43	kidneybeans
4	152	81	69	44	kidneybeans
2	153	82	70	45	kidneybeans
3	154	83	71	46	kidneybeans
4	155	84	72	47	kidneybeans
5	156	85	73	48	kidneybeans
6	157	86	74	49	kidneybeans
7	158	87	75	50	kidneybeans
2	159	88	76	51	kidneybeans
3	160	89	77	52	kidneybeans
4	161	90	78	53	kidneybeans
5	162	91	79	54	kidneybeans
6	163	92	80	55	kidneybeans
4	164	93	81	56	kidneybeans
5	165	94	82	57	kidneybeans
6	166	95	83	58	kidneybeans
7	167	96	84	59	kidneybeans
2	168	97	85	60	kidneybeans
3	169	98	86	61	kidneybeans
4	170	99	87	62	kidneybeans
3	110	21	31	11	pigeonpeas
4	111	22	32	12	pigeonpeas
2	112	23	33	13	pigeonpeas
3	113	24	34	14	pigeonpeas
4	114	25	35	15	pigeonpeas
5	115	26	36	16	pigeonpeas
6	116	27	37	17	pigeonpeas
7	117	28	38	18	pigeonpeas
2	118	29	39	19	pigeonpeas
3	119	30	40	20	pigeonpeas
4	120	31	41	21	pigeonpeas
5	121	32	42	22	pigeonpeas
6	122	33	43	23	pigeonpeas
4	123	34	44	24	pigeonpeas
5	124	35	45	25	pigeonpeas
6	125	36	46	26	pigeonpeas
7	126	37	47	27	pigeonpeas
1	127	38	48	28	pigeonpeas
2	128	39	49	29	pigeonpeas
3	129	40	50	30	pigeonpeas
4	130	41	51	31	pigeonpeas
5	131	42	52	32	pigeonpeas
6	132	43	53	33	pigeonpeas
7	133	44	54	34	pigeonpeas
2	134	45	55	35	pigeonpeas
2	135	46	56	36	pigeonpeas
3	136	47	57	37	pigeonpeas
4	137	48	58	38	pigeonpeas
5	138	49	59	39	pigeonpeas
6	139	50	60	40	pigeonpeas
7	140	51	61	41	pigeonpeas
2	141	52	62	42	pigeonpeas
3	142	53	63	43	pigeonpeas
4	143	54	64	44	pigeonpeas
5	144	55	65	45	pigeonpeas
6	145	56	66	46	pigeonpeas
4	146	57	67	47	pigeonpeas
5	147	58	68	48	pigeonpeas
6	148	59	69	49	pigeonpeas
7	149	60	70	50	pigeonpeas
2	150	61	71	51	pigeonpeas
3	151	62	72	52	pigeonpeas
4	152	63	73	53	pigeonpeas
2	153	64	74	54	pigeonpeas
3	154	65	75	55	pigeonpeas
4	155	66	76	56	pigeonpeas
5	156	67	77	57	pigeonpeas
6	157	68	78	58	pigeonpeas
4	158	69	79	59	pigeonpeas
5	159	70	80	60	pigeonpeas
6	160	71	81	61	pigeonpeas
7	100	30	40	25	mothbeans
2	101	31	41	26	mothbeans
3	102	32	42	27	mothbeans
4	103	33	43	28	mothbeans
2	104	34	44	29	mothbeans
3	105	35	45	30	mothbeans
4	106	36	46	31	mothbeans
5	107	37	47	32	mothbeans
6	108	38	48	33	mothbeans
7	109	39	49	34	mothbeans
2	110	40	50	35	mothbeans
3	111	41	51	36	mothbeans
4	112	42	52	37	mothbeans
5	113	43	53	38	mothbeans
6	114	44	54	39	mothbeans
4	115	45	55	40	mothbeans
5	116	46	56	41	mothbeans
6	117	47	57	42	mothbeans
7	118	48	58	43	mothbeans
2	119	49	59	44	mothbeans
3	120	50	60	45	mothbeans
4	121	51	61	46	mothbeans
3	122	52	62	47	mothbeans
4	123	53	63	48	mothbeans
2	124	54	64	49	mothbeans
3	125	55	65	50	mothbeans
4	126	56	66	51	mothbeans
5	127	57	67	52	mothbeans
6	128	58	68	53	mothbeans
7	129	59	69	54	mothbeans
2	130	60	70	55	mothbeans
3	131	61	71	56	mothbeans
4	132	62	72	57	mothbeans
5	133	63	73	58	mothbeans
6	134	64	74	59	mothbeans
4	135	65	75	60	mothbeans
5	136	66	76	61	mothbeans
6	137	67	77	62	mothbeans
7	138	68	78	63	mothbeans
1	139	69	79	64	mothbeans
2	140	70	80	65	mothbeans
3	141	71	81	66	mothbeans
4	142	72	82	67	mothbeans
5	143	73	83	68	mothbeans
6	144	74	84	69	mothbeans
7	145	75	85	70	mothbeans
2	146	76	86	71	mothbeans
2	147	77	87	72	mothbeans
3	148	78	88	73	mothbeans
4	149	79	89	74	mothbeans
5	150	80	90	75	mothbeans
6	100	81	30	21	mungbean
7	110	82	31	22	mungbean
2	111	83	32	23	mungbean
3	112	84	33	24	mungbean
4	113	85	34	25	mungbean
5	114	86	35	26	mungbean
6	115	87	36	27	mungbean
4	116	88	37	28	mungbean
5	117	89	38	29	mungbean
6	118	90	39	30	mungbean
7	119	91	40	31	mungbean
2	120	92	41	32	mungbean
3	121	93	42	33	mungbean
4	122	22	43	34	mungbean
2	123	23	44	35	mungbean
3	124	24	45	36	mungbean
4	125	25	46	37	mungbean
5	126	26	47	38	mungbean
6	127	27	48	39	mungbean
4	128	28	49	40	mungbean
5	129	29	50	41	mungbean
6	130	30	51	42	mungbean
7	131	31	52	43	mungbean
2	132	32	53	44	mungbean
3	133	33	54	45	mungbean
4	134	34	55	46	mungbean
2	135	35	56	47	mungbean
3	136	36	57	48	mungbean
4	137	37	58	49	mungbean
5	138	38	59	50	mungbean
6	139	39	60	51	mungbean
7	140	40	61	52	mungbean
2	141	41	62	53	mungbean
3	142	42	63	54	mungbean
4	143	43	64	55	mungbean
5	144	44	65	56	mungbean
6	145	45	66	57	mungbean
4	146	46	67	58	mungbean
5	147	47	68	59	mungbean
6	148	48	69	60	mungbean
7	149	49	70	61	mungbean
2	150	50	71	62	mungbean
3	151	51	72	63	mungbean
4	152	52	73	64	mungbean
3	153	53	74	65	mungbean
4	154	54	75	66	mungbean
2	155	55	76	67	mungbean
3	156	56	77	68	mungbean
4	157	57	78	69	mungbean
5	158	58	79	70	mungbean
6	159	59	80	71	mungbean
7	100	63	32	30	blackgram
2	101	64	33	32	blackgram
3	102	65	34	34	blackgram
4	103	66	35	36	blackgram
5	104	67	36	38	blackgram
6	105	68	37	40	blackgram
4	106	69	38	42	blackgram
5	107	70	39	44	blackgram
6	108	71	40	46	blackgram
7	109	72	41	48	blackgram
2	110	73	42	50	blackgram
3	111	74	43	52	blackgram
4	112	75	44	54	blackgram
5	113	76	45	56	blackgram
6	114	77	46	58	blackgram
4	115	78	47	60	blackgram
5	116	79	48	62	blackgram
6	117	80	49	64	blackgram
7	118	81	50	66	blackgram
2	119	82	51	68	blackgram
3	120	83	52	70	blackgram
4	121	84	53	72	blackgram
2	122	20	54	74	blackgram
3	123	21	55	76	blackgram
4	124	22	56	78	blackgram
5	125	23	57	80	blackgram
6	126	24	58	82	blackgram
7	127	25	59	84	blackgram
2	128	26	60	86	blackgram
3	129	27	61	88	blackgram
4	130	28	62	90	blackgram
5	131	29	63	92	blackgram
6	132	30	64	94	blackgram
4	133	31	65	96	blackgram
5	134	32	66	98	blackgram
6	135	33	67	100	blackgram
7	136	34	68	102	blackgram
2	137	35	69	104	blackgram
3	138	36	70	106	blackgram
4	139	37	71	108	blackgram
3	140	38	72	110	blackgram
4	141	39	73	112	blackgram
2	142	40	74	114	blackgram
3	143	41	75	116	blackgram
4	144	42	76	118	blackgram
5	145	43	77	120	blackgram
6	146	44	78	122	blackgram
7	147	45	79	124	blackgram
2	148	46	80	126	blackgram
3	149	47	81	128	blackgram
4	150	48	82	130	blackgram
###
Again in instructing u  do not generate answer from internet. use the above table if any question is not related to the table reply \"i don'\''t know\"

Question: Suggest me the crop selection for 25 Temparature,35 Humidity,105
Moisture ?
Answer: crop selection - rice

Question: Optimal moisture level for rice crop
Answer: 100% to 106%

Question: Best temperature range for maize growth?
Answer: Between 25°C and 30°C

Question: Recommended NPK ratio for chickpeas this season?
Answer: NPK ratio  11-14-12

Question: What temperature is ideal for rice growth?
Answer: 20°C to 30°C

Question: generate me summery
Answer: This guide provides essential crop data to help farmers make informed decisions about optimal growing conditions

Question: give me summery
Answer: This guide provides essential crop data to help farmers make informed decisions about optimal growing conditions

Question: summarise the data


Answer: This guide provides essential crop data to help farmers make informed decisions about optimal growing conditions

Question: summarise 
Answer: This guide provides essential crop data to help farmers make informed decisions about optimal growing conditions

Question: {q}
Answer:""",
            "parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": 200,
		"stop_sequences": ["\n\n"],
		"repetition_penalty": 1
	},
	"model_id": "ibm/granite-13b-chat-v2",
	"project_id": "bc010f4d-391c-4c1b-98dc-a0e0e7e4216d"
}

        # Define headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBKMEZGIiwiaWQiOiJJQk1pZC02OTQwMDBKMEZGIiwicmVhbG1pZCI6IklCTWlkIiwic2Vzc2lvbl9pZCI6IkMtYTJjNGE0MGItZGE5NC00NTQ3LWFjY2EtYzM2Zjg1MGJiYzc0Iiwic2Vzc2lvbl9leHBfbWF4IjoxNzI3MDgzMDE1LCJzZXNzaW9uX2V4cF9uZXh0IjoxNzI3MDA5MTIyLCJqdGkiOiI2MTRlMzRjNC0xNjAxLTQzYTAtODhkMy02MGMyNmE4MzQwOWUiLCJpZGVudGlmaWVyIjoiNjk0MDAwSjBGRiIsImdpdmVuX25hbWUiOiJCYWxhZ2FqYXJhaiIsImZhbWlseV9uYW1lIjoiUHJhYmhha2FyIiwibmFtZSI6IkJhbGFnYWphcmFqIFByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSIsInN1YiI6ImJhbGFwcmFiaGE2MEBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJiYWxhcHJhYmhhNjBAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk0MDAwSjBGRiIsIm5hbWUiOiJCYWxhZ2FqYXJhaiBQcmFiaGFrYXIiLCJnaXZlbl9uYW1lIjoiQmFsYWdhamFyYWoiLCJmYW1pbHlfbmFtZSI6IlByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJjNjkzNTFiNGNjYjk0MmRlOTAzMzJkNWUzOTMyYWI3NCIsImltc191c2VyX2lkIjoiMTI2ODc5NTciLCJpbXMiOiIyNzUwMjIyIn0sImlhdCI6MTcyNzAwMTkxOSwiZXhwIjoxNzI3MDAzMTE5LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6cGFzc2NvZGUiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJieCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.VQq4ZdWOmm_RoZaM-gcv7kyzRzunnSrvXjgPnD8bFHQCNFNfQaXrDyG5EHOlo8Jj04p6Bbpvk7u5UHsKYaFtbRhjDn8BWLIz6f8S914pPf4fJ9VWUKDPoL3cykhB4K5uhXnHLMVxuOKvCaoizd2e85PgZuhDK9WREtvAiPi9lheercV2e9wY2dkc358DAuY0SACT2mQMoA6wpbz8EyZkG8psSSQOWmDSiqSsDvWlaisqmFnp0z4CyWZArmC-Dr3U-L6sEQjk_p8kKWlaXlrJLnmdJ3rBb8UYV6ppCaEaZoppniSIXFcVE-ldGrEiTgfASQzHHAL9NCXcR8o74MtHZQ"
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
