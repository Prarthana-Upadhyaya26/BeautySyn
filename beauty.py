"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import streamlit as st
import google.generativeai as genai
import time
import serial

try:
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM5'
    ser.open()
    item_id= ser.read(12)
    print(item_id)
    ser.close()
    # Do something with the serial connection
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")

# Configure page
st.set_page_config(
    page_title="SKINSYNC",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');
        
        body {
            background-color: white;
            color: black;
        }
        
        .stApp {
            background-color: white;
        }.scan-button {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #5f9ea0;
            font-size: 1.2em;
            background-color: black;
            padding: 5px 10px;
            border-radius: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
            
        
        
        .title {
            font-family: 'Oswald', sans-serif;
            font-size: 5em;
            font-weight: 700;
            color: black;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            text-align: center;
            margin-top: 2rem;
            # margin-bottom: -1rem;
        }
        
        .scan-button {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: white;
            font-size: 1.2em;
        }
        
        .form-container {
            background-color: #5f9ea0;
            border-radius: 100px 100px 0 0;
            padding: 2rem;
            margin-top: -50px;
            color: white;
            text-align: center;
        }
            
        .form-title-container {
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: black;
            font-size: 1.2em;
            background-color: white;
            padding: 5px 10px;
            border-radius: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .form-container label {
            color: black !important; /* Change label text color to black */
            font-size: 16px; /* Optional: Adjust font size */
            font-weight: bold; /* Optional: Make it bold */
        }
        
        .stTextInput input {
            color: black !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 20px !important;
            margin: 10px !important;
            width: 300px !important;
        }
        
        .stButton > button {
            background-color: #5f9ea0 !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 40px !important;
            margin-top: 20px !important;
            font-weight: bold !important;
        }
        
        .results-container {
            background-color: #5f9ea0 !important;
            font-size: 1em;
            text-align: left;
            margin-bottom: 1rem;
            font-family: 'Oswald', sans-serif;
            color: white
        }
        
        .results-title {
            background-color: #5f9ea0 !important;
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 1rem;
            font-family: 'Oswald', sans-serif;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# Header with title and scan button
st.markdown("""
    <div class="title-container">
        <h1 class="title">SKINSYNC</h1>
        <div class="scan-button">
            <span>📸</span>
            <span>scan to add to cart</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Load and display images
col1, col2, col3 = st.columns([1,1,1])

# Replace these with your actual image paths
image1 = "./images/image 2.jpg"
image2 = "./images/image1.jpg"
image3 = "./images/image3.jpg"

with col1:
    st.image(image1, use_column_width=True)
with col2:
    st.image(image2, use_column_width=True)
with col3:
    st.image(image3, use_column_width=True)

# Product input form
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown("""
            <div class="form-title-container">',
                <h3>Add product 1</h3>
            </div>
""", unsafe_allow_html=True)
product1 = st.text_input("Add product 1", key="product1")
product2 = st.text_input("Add product 2", key="product2")
submit_button = st.button("SUBMIT")
st.markdown('</div>', unsafe_allow_html=True)


# Keep the existing Gemini AI configuration
GEMINI_API_KEY = "" #Replace with your gemini api key
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Existing model configuration
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a experienced saleswoman in a beauty shop with all the knowledge of cosmetics. Recommend items and products that compliments the current selection in the cart, be friendly, cheerful and polite.",
)

# Modified get_recommendations function
def get_recommendations(item1, item2):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [f"I have {item1} and {item2} in my cart"],
            },
            {
                "role": "user",
                "parts": ["Please do not ask me questions at the end."]
            },
            {
                "role": "user",
                "parts": ["Give me the products point wise along with it's description."]
            }
        ]
    )
    response = chat_session.send_message(f"I have added {item1} and {item2} in my cart. Suggest me some products.")
    
    # Display results in styled container
    st.markdown("""
        <div class="results-container">
            <div class="results-title">WE KNOW WHAT YOU LIKE!</div>
            <div class="results-container">
                {}
            </div>
        </div>
    """.format(response.text.replace("*", "<strong>").replace("\n", "<br>").replace("<strong>", "<strong>").replace("</strong>", "</strong>")), unsafe_allow_html=True)


# Handle form submission
if submit_button:
    if product1 and product2:
        get_recommendations(product1, product2)
    else:
        st.warning("Please enter both products before submitting.")