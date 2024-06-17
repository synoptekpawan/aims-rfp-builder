# streamlit version 1.32.2
import streamlit as st
import yaml
import streamlit_authenticator as stauth
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
from src.Generate_RFP_Response import generateRfpResponse
from src.Query_RFP_Request import queryRfp
from src.feedback import display_feedback_form
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

st.sidebar.image(r"./synoptek-new-removebg-3.png")

with st.sidebar:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        #config['preauthorized']
    )

    if "name" not in st.session_state:
        st.session_state.name = None

    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "Home"

    # Authentication
    name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    st.sidebar.markdown(f'## Hello *{st.session_state["name"]}*')

    # Sidebar menu selection
    selected = option_menu(
        menu_title=None,
        options=['Home', 'Generate RFP Response', 'Query RFP Response',],# 'Feedback'],
        icons=['house', 'cloud-upload', 'list-task',],# 'chat'],
        menu_icon="cast", default_index=-1, orientation="horizontal",
        key="selected_menu"
    )

    # Use selected option directly without modifying session state
    selected_menu = st.session_state.selected_menu

    # Operation
    if selected_menu == "Home":
        st.write("# Welcome to RFP Builder! 👋")
        st.markdown(
            """
            Welcome to our Streamlit-powered Request for Proposal (RFP) Management System. 
            Our platform streamlines the RFP process, offering a seamless experience from 
            request QnA to response generation.
            
            **👈 Login to see a demo from the sidebar** to see some examples
            of what RFP Builder can do!
            #### Key Features!
            -   **RFP QnA**: Chat with RFP request to extract insights, ensuring clarity and responsiveness throughout 
            the RFP lifecycle.
            -   **Response Generation**: Simplify the creation of RFP responses by providing predefined 
            templates and customizable sections. MSPs can efficiently address each requirement 
            outlined in the RFP request, ensuring comprehensive and accurate responses.
            -   **Sectioned Response Creation**: Our platform supports the creation of structured responses, 
            allowing MSPs to address each section and subsection of the RFP request systematically. 
            This ensures clarity and completeness in the delivered responses.
            """
        )

    elif selected_menu == "Generate RFP Response":
        generateRfpResponse()

    elif selected_menu == "Query RFP Response":
        queryRfp()

    elif selected_menu == "Feedback":
        display_feedback_form()

    authenticator.logout('Logout', 'sidebar')

else:

    if st.session_state["authentication_status"] == False:
        st.sidebar.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.sidebar.warning('Please enter your username and password')

    # Display welcome text if not authenticated
    st.write("# Welcome to RFP Builder! 👋")
    st.markdown(
        """
        Welcome to our Streamlit-powered Request for Proposal (RFP) Management System. 
        Our platform streamlines the RFP process, offering a seamless experience from 
        request QnA to response generation.
        
        **👈 Login to see a demo from the sidebar** to see some examples
        of what RFP Builder can do!
        #### Key Features!
        -   **RFP QnA**: Chat with RFP request to extract insights, ensuring clarity and responsiveness throughout 
            the RFP lifecycle.
        -   **Response Generation**: Simplify the creation of RFP responses by providing predefined 
            templates and customizable sections. MSPs can efficiently address each requirement 
            outlined in the RFP request, ensuring comprehensive and accurate responses.
        -   **Sectioned Response Creation**: Our platform supports the creation of structured responses, 
            allowing MSPs to address each section and subsection of the RFP request systematically. 
            This ensures clarity and completeness in the delivered responses.
        """
    )
