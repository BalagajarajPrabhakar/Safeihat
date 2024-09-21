import streamlit as st
import requests
import subprocess

def get_iam_token():
        
        result = subprocess.run(
            ['ibmcloud', 'iam', 'oauth-tokens'],
            capture_output=True,
            text=True,
            check=False
        )
        a=result.stdout

        # Print raw output for debugging
        return a[19:1597]
# Set up the title of the app
#token = get_iam_token()
st.write(token)
st.title("Tomato Information Generator")

# Input for the user's question
q = st.text_input("Enter your question:")

# Button to submit the question
if st.button("Submit"):
    if q and token:
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

        # Define headers, make sure to add your API key
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization":"Bearer eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBKMEZGIiwiaWQiOiJJQk1pZC02OTQwMDBKMEZGIiwicmVhbG1pZCI6IklCTWlkIiwic2Vzc2lvbl9pZCI6IkMtZGRiMDA2MWMtMWIzYS00MzU4LTkwNzYtNWFmMTA3ZTZlMDUxIiwic2Vzc2lvbl9leHBfbWF4IjoxNzI2OTcwNTc4LCJzZXNzaW9uX2V4cF9uZXh0IjoxNzI2OTAxNTc1LCJqdGkiOiIyYTQ0NDIzZC05ODRjLTRlMmQtYWViYS1lOWMxNGQyNTM3YWEiLCJpZGVudGlmaWVyIjoiNjk0MDAwSjBGRiIsImdpdmVuX25hbWUiOiJCYWxhZ2FqYXJhaiIsImZhbWlseV9uYW1lIjoiUHJhYmhha2FyIiwibmFtZSI6IkJhbGFnYWphcmFqIFByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSIsInN1YiI6ImJhbGFwcmFiaGE2MEBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJiYWxhcHJhYmhhNjBAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk0MDAwSjBGRiIsIm5hbWUiOiJCYWxhZ2FqYXJhaiBQcmFiaGFrYXIiLCJnaXZlbl9uYW1lIjoiQmFsYWdhamFyYWoiLCJmYW1pbHlfbmFtZSI6IlByYWJoYWthciIsImVtYWlsIjoiYmFsYXByYWJoYTYwQGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJjNjkzNTFiNGNjYjk0MmRlOTAzMzJkNWUzOTMyYWI3NCIsImltc191c2VyX2lkIjoiMTI2ODc5NTciLCJpbXMiOiIyNzUwMjIyIn0sImlhdCI6MTcyNjg5NDM3MiwiZXhwIjoxNzI2ODk1NTcyLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6cGFzc2NvZGUiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJieCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.oUZ8QfNhoJ1VsXF46Mz6kqODVVJ61OjVhbaRXTU-Pjx74E0q40F4l2GoSAAG_vLT023LqUWkHmBB5HfMkO1HeLETgR109LNP-KB9FpIHa0XJIR2SLtYiAdIaLGb2zRam00HOpGEQV8A5DpfATJrn08QK4glCE7FAIMJQEWutJxjR4tdmvPqxj4u4fYSMY1sh_EeBmMiVocjonoJlnWi9ZETuQYxzY7E0zKLdfREiAxXa1YqtNT5tNwXshRhgJOwY35KrKf0IXs1BTk7kbHGoVYnUVDGQmGJN66cliwDPL__NtGKoH7AMDLbttHDhgrVBmINkh43WPuM2vdkUNaCDAQ"
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
