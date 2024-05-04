# streamlit version 1.32.2
import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

add_logo(r"./synoptek-new-removebg-3.png")
st.sidebar.markdown("")

st.write("# Welcome to RFP Builder! 👋")

# st.sidebar.success("Select a Task.")


st.markdown(
    """
    Welcome to our Streamlit-powered Request for Proposal (RFP) Management System. 
    Our platform streamlines the RFP process, offering a seamless experience from 
    request QnA to response generation.
    
    **👈 Select a demo from the sidebar** to see some examples
    of what RFP Builder can do!
    #### Key Features!
    -   Chat and Query Functionality: Enable seamless communication between clients and MSPs 
        through built-in chat and query features, ensuring clarity and responsiveness throughout 
        the RFP lifecycle.
    -   Response Generation: Simplify the creation of RFP responses by providing predefined 
        templates and customizable sections. MSPs can efficiently address each requirement 
        outlined in the RFP request, ensuring comprehensive and accurate responses.
    -   Sectioned Response Creation: Our platform supports the creation of structured responses, 
        allowing MSPs to address each section and subsection of the RFP request systematically. 
        This ensures clarity and completeness in the delivered responses.
"""
)

