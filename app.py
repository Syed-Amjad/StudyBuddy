import os
from groq import Groq
import streamlit as st
from datetime import datetime

# Set up the environment for the Groq API key
os.environ['GROQ_API_KEY'] = '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'

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define the Streamlit UI with a professional layout
st.set_page_config(page_title="Personalized Study Assistant", layout="centered")
st.title("📚 StudyBuddy")
st.markdown("Welcome to your personalized study planning assistant! Enter your details to receive customized study tips and resources.")

# User inputs for study customization
with st.form(key='study_form'):
    study_subject = st.text_input("📖 Enter your study subject:")
    exam_date = st.date_input("📅 Enter your exam date:")
    daily_hours = st.number_input("⏰ Hours you can dedicate each day:", min_value=1, max_value=24, step=1)
    
    # Submit button to trigger the API call
    submit_button = st.form_submit_button(label="Generate Study Plan")

# Calculate remaining days for preparation and display study plan if the form is submitted
if submit_button:
    if study_subject and exam_date and daily_hours:
        days_remaining = (exam_date - datetime.today().date()).days

        # Create messages for the Groq chat completion
        messages = [
            {
                "role": "user",
                "content": f"Provide study tips and resources for {study_subject}. "
                           f"I have {days_remaining} days to prepare and can dedicate {daily_hours} hours each day."
            }
        ]

        # Make the API call
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192"
            )

            # Extract and display the response
            study_plan = chat_completion.choices[0].message.content
            st.subheader("📅 Your Personalized Study Plan and Tips")
            st.write(study_plan)

        except Exception as e:
            st.error(f"Failed to retrieve data from Groq API. Please check your API key or try again later.\n\nError: {e}")
    else:
        st.warning("Please fill out all fields to generate your study plan.")

# Footer with attribution
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.85em; font-style: italic;'>This App is made by Syed Amjad Ali</p>", unsafe_allow_html=True)
