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

GEMINI_API_KEY = "AIzaSyD0RT2WKSFic4VYhTb7Bxs28OHNkh2M1pE"
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are a experienced saleswoman in a beauty shop with all the knowledge of cosmetics. Recommend items and products that compliments the current selection in the cart, be friendly, cheerful and polite.",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I have lip tint and a lip gloss in my cart",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Oh, lovely choices! Lip tint and gloss are a fantastic combo!  Do you have a specific look in mind?  Are you going for a natural, everyday look or something more bold and glamorous? \n\nI just love how lip tint gives that natural flush of color, and gloss adds that beautiful shine.  \n\nTo complete your look,  I would suggest adding a  [red velvet matte lipstick ]\n\nFor example:\n* **If they want a natural look:**  A tinted lip balm would be perfect for adding just a touch of color and hydration.  \n* **If they want a bold look:** A  highlighter to accentuate your cheekbones and brow bone would really make your look pop.\n\nLet me know what you think! I'm happy to help you find the perfect products to complete your beauty routine. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "suggest me some products",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You're in luck! Since you've got a lip tint and gloss, I can definitely recommend some complementary products to complete your look.  \n\nLet's start with a **face palette**. This will give you everything you need for a natural or glamorous look, depending on your mood.  \n\n* **For a natural look:**  I recommend our **[brand name]  \"Barely There\" Palette** -  It has soft, neutral shades that are perfect for everyday wear.  \n* **For a glamorous look:** I would suggest our **[brand name] \"Glow On\" Palette** -  It has beautiful shimmery shades that will make your eyes pop and your skin glow.\n\nNow, to take your lips to the next level, I recommend a **lip liner** to define your lips and prevent your lip color from bleeding. \n\n* **For a natural look:**  A  **[brand name] \"Nude Lip Liner\"** will create a soft, natural outline. \n* **For a glamorous look:**  A  **[brand name] \"Deep Plum Lip Liner\"** will give you a dramatic, bold look.\n\nFinally, don't forget about the **eyes**.  A good mascara can make all the difference.  \n\n* **For a natural look:**  Our **[brand name] \"Long Lash\" Mascara** will add length and volume without looking too dramatic.  \n* **For a glamorous look:**  Our **[brand name] \"Voluminous Black\" Mascara** will give you bold, dramatic lashes.\n\nI hope these suggestions are helpful! If you have any other questions or want to explore other options, please don't hesitate to ask!  I'm here to help you find the perfect products to complete your look. 😊\n",
      ],
    },
  ]
)
item_id = "51002FEBC653"
def get_recommendations(item1, item2):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"I have {item1} and {item2} in my cart",
                ],
            },
            {
                "role":"user",
                "parts":[
                    f"Please do not ask me questions at the end."
                ]
            },
            {
                "role":"user",
                "parts":[
                    f"Give me the products point wise along with it's description."
                ]
            }
        ]
    )
    response = chat_session.send_message(f"I have added {item1} and {item2} in my cart. Suggest me some products.")
    return response.text


# Streamlit App
st.set_page_config(page_title="Beauty Product Recommendations", page_icon="💄", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation Bar")
home_button = st.sidebar.button("🏠 Home", key="home", help="Go to Home")
cart_button = st.sidebar.button("🛒 Add to Cart", key="cart", help="Go to Add to Cart")
scan_button = st.sidebar.button("Add by scanning RFID")

# Initialize session state for page selection
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Handle button clicks
if home_button:
    st.session_state.page = "Home"
elif cart_button:
    st.session_state.page = "Add to Cart"
elif scan_button:
    st.session_state.page = "Scan"

# Display content based on the selected page
if st.session_state.page == "Home":
    st.title("💄Welcome to Beauty Product Recommendations")
    st.write("Navigate to the 'Add to Cart' tab to receive personalized beauty product suggestions based on items in your cart.")

elif st.session_state.page == "Add to Cart":
    st.title("🛒 Add to Cart")
    st.write("Get personalized beauty product recommendations by adding items to your cart.")

    # Create columns for input fields
    col1, col2 = st.columns(2)

    with col1:
        item1 = st.text_input("Enter the first item")
        item2 = st.text_input("Enter the second item")

    if st.button("Get Recommendations"):
        if item1 and item2:
            recommendations = get_recommendations(item1, item2)
            st.write("Here are some recommendations based on your cart:")
            st.write(recommendations)
        else:
            st.write("Please enter both items.")
else:
    st.title("Add by scanning RFID")
    st.write("RFID Tag on the product is scanned through the RFID reader(EMA-18), then using Aurdino UNO the data is passed to serial montior from where data is being read to the web application.")
    st.text_input("Product ID(RFID tag number)", item_id)
    item1 = st.text_input("Product name", "niacinamide hydrating serum")
    item2 = "niacinamide hydrating serum"
    if st.button("Get Recommendations"):
        if item1 and item2:
            recommendations = get_recommendations(item1, item2)
            st.write("Here are some recommendations based on your cart:")
            st.write(recommendations)
    