# **Beauty Product Recommendation System with RFID Integration**

## Overview
This project is a **Streamlit-based web application** integrated with **Google AI Generative API** (Gemini-1.5) to provide personalized beauty product recommendations. The system leverages the power of **Large Language Models (LLMs)**, particularly the Gemini-1.5 model, to analyze user input and generate tailored product suggestions. It also incorporates an RFID-based system to scan product IDs for enhanced shopping experiences.

The AI assistant is modeled as a knowledgeable beauty shop salesperson, offering personalized and context-aware suggestions to enhance customer choices. The system allows product recommendations either by manual input or RFID scanning, ensuring a seamless shopping experience powered by AI-driven insights.

---
## Features
1. **Personalized Beauty Product Recommendations**:
   - Uses **Google Generative AI (Gemini-1.5)** to recommend complementary beauty products based on items in the cart.
   - Provides suggestions with detailed descriptions in a user-friendly format.

2. **RFID Integration**:
   - Scans RFID tags via an **EMA-18 RFID reader** connected to an **Arduino UNO**.
   - Automatically fetches product information to suggest complementary items.

3. **Streamlit UI**:
   - Modern, interactive user interface with navigation options:
     - **Home**: Overview of the app.
     - **Add to Cart**: Manual entry of items to get recommendations.
     - **Scan RFID**: Use RFID to add items to the cart.

4. **Python-Arduino Communication**:
   - Serial communication between Python and Arduino to read RFID data and pass it to the web app.

---

## Large Language Model (LLM) Integration

The **Google Generative AI (Gemini-1.5)** model powers the personalized beauty product recommendations in this system. Gemini-1.5 is a **Large Language Model (LLM)** that utilizes deep learning to understand complex user input and context. In this application, the LLM:

- **Analyzes User Inputs**: It processes the items added to the shopping cart (either manually or via RFID scanning) and suggests complementary beauty products that fit the user’s preferences.
- **Generates Descriptive Suggestions**: Each recommendation is accompanied by a detailed description of the product, ensuring that users can make informed choices.
- **Enhances User Experience**: The LLM simulates a personalized, interactive shopping assistant, providing a seamless and responsive shopping experience.

The **Gemini-1.5 model** is fine-tuned to generate relevant product recommendations, enabling the system to understand various beauty product categories, user preferences, and trends, making the recommendation engine intuitive and highly responsive.

---

## System Requirements
- **Hardware**:
  - RFID Reader (e.g., EMA-18)
  - Arduino UNO
  - Product tags with RFID
- **Software**:
  - Python 3.8+
  - Streamlit
  - Google Generative AI Python SDK
  - Arduino IDE

---

## Installation and Setup

### Python Setup
1. **Install required Python libraries**:
   ```bash
   pip install streamlit google-generativeai pyserial
   ```

2. **Set up the Google AI SDK**:
   - Install the SDK:
     ```bash
     pip install google-generativeai
     ```
   - Configure the API key:
     Replace `GEMINI_API_KEY` in the script with your API key from Google AI.

### Arduino Setup
1. **Upload the following Arduino code** to your Arduino board:
   ```cpp
   char input[12];
   int count = 0;

   void setup() {
     Serial.begin(9600); // START SERIAL AT BAUD RATE OF 9600 BITS/SEC
   }

   void loop() {
     if (Serial.available()) { // CHECK FOR AVAILABILITY OF SERIAL DATA
       count = 0; // Reset the counter to zero

       while (Serial.available() && count < 12) {
         input[count] = Serial.read(); // Read 1 Byte of data and store it in the input[] variable
         count++; // increment counter
         delay(5);
       }

       // PRINTING RFID TAG
       for (int i = 0; i < 12; i++) {
         Serial.print(input[i]);
       }
       Serial.println();
     }
   }
   ```

2. Connect the RFID reader to the Arduino UNO as per the hardware configuration.

---

## Usage

### Running the Streamlit App
1. Run the app using Streamlit:
   ```bash
   streamlit run beauty.py
   ```

2. Navigate through the tabs:
   - **Home**: Learn about the app.
   - **Add to Cart**: Enter two products manually to get recommendations.
   - **Scan RFID**: Use the RFID reader to scan product IDs and fetch recommendations.

### Recommendation Workflow
- For manual entry:
  - Enter product names in the `Add to Cart` section and click "Get Recommendations."
- For RFID scanning:
  - Connect the RFID reader, scan the tag, and click "Get Recommendations."

### AI Recommendations
- The recommendations are generated based on the products in the cart.
- Suggestions are presented in a point-wise format with detailed descriptions.

---

## File Structure
- `beauty.py`: Main Python script for the Streamlit app.
- `rfid_scanner.ino`: Arduino code to read RFID tags.

---

## Notes
1. **RFID Integration**:
   - Ensure the correct COM port is used in the Python script (`ser.port = 'COM5'`).
   - Adjust delay timings in Arduino code if the RFID data is not read correctly.

2. **Google Generative AI Configuration**:
   - Replace the placeholder API key with a valid key.

---

## Future Improvements
- Expand AI recommendations to include product images and links.
- Enable multi-product scanning using RFID.
- Incorporate inventory management using a database.

---

## Credits
- **Google Generative AI** for providing personalized recommendations.
- **Arduino** for seamless hardware integration.
- **Streamlit** for creating an intuitive web interface.

---
