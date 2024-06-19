# feedback_form.py
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import os

def display_feedback_form(excel_file="feedback.xlsx"):
    """
    Display the feedback form and handle submission.

    Args:
    - excel_file (str): The path to the Excel file where feedbacks will be stored.
    """
    # Set page configuration
    # st.set_page_config(page_title="Feedback Form", page_icon="📝", layout="centered")

    # Page title
    st.title("Feedback Form")

    # Collecting user inputs
    name = st.text_input("Name")
    email = st.text_input("Email")
    rating = st.slider("Rate your experience", 1, 5)
    comments = st.text_area("Comments")

    # Submit button
    if st.button("Submit"):
        # Validate inputs
        if name and email and comments:
            # Create a dictionary with the feedback
            feedback = {
                "Name": [name],
                "Email": [email],
                "Rating": [rating],
                "Comments": [comments]
            }

            # Convert dictionary to DataFrame
            feedback_df = pd.DataFrame(feedback)

            # Append feedback to the Excel file
            if not os.path.isfile(excel_file):
                # If file does not exist, create it
                feedback_df.to_excel(excel_file, index=False, sheet_name='Feedback')
            else:
                # If file exists, append to the existing sheet
                with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    workbook = writer.book
                    worksheet = writer.sheets['Feedback']
                    start_row = worksheet.max_row
                    feedback_df.to_excel(writer, index=False, header=False, startrow=start_row)

            st.success("Thank you for your feedback!")
        else:
            st.error("Please fill out all fields.")

# if __name__ == "__main__":
#     display_feedback_form()
