# streamlit version 1.32.2
import streamlit as st
from streamlit_extras.app_logo import add_logo
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from src.Generate_RFP_Response import generate_rfp_response
from src.Query_RFP_Request import query_rfp_request

st.set_page_config(
    page_title="Hello",
    page_icon="👋", 
    layout="wide"
)

# Load configuration file
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Configuration file not found. Please upload 'config.yaml'.")
    st.stop()
except yaml.YAMLError as e:
    st.error(f"Error parsing configuration file: {e}")
    st.stop()

# Sidebar content
st.sidebar.image(r"./synoptek-new-removebg-3.png")

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    # config['preauthorized']  # Ensure to handle this if needed
)

if "name" not in st.session_state:
    st.session_state.name = None
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None
if "username" not in st.session_state:
    st.session_state.username = None

# Authentication
with st.sidebar:
    name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Generate RFP Response", "Query RFP Request"],
        icons=['house', 'cloud-upload', "list-task"], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal"
    )

    # --- APP ---   
    # operation
    if selected == "Home":
        st.write("# Welcome to RFP Builder! 👋")
        st.markdown(
            """
            Welcome to our Streamlit-powered Request for Proposal (RFP) Management System. 
            Our platform streamlines the RFP process, offering a seamless experience from 
            request QnA to response generation.

            **👈 Login and Select a demo from the sidebar** to see some examples
            of what RFP Builder can do!
            #### Key Features!
            - Chat and Query Functionality: Enable seamless chat and query from RFP request documents 
              through built-in chat and query features, ensuring clarity and responsiveness throughout 
              the RFP lifecycle.
            - Response Generation: Simplify the creation of RFP responses by providing predefined 
              templates and customizable sections. MSPs can efficiently address each requirement 
              outlined in the RFP request, ensuring comprehensive and accurate responses.
            - Sectioned Response Creation: Our platform supports the creation of structured responses, 
              allowing MSPs to address each section and subsection of the RFP request systematically. 
              This ensures clarity and completeness in the delivered responses.
            """
        )
        st.sidebar.markdown("""<div style="height: 5vh;"></div>""", unsafe_allow_html=True)
        st.sidebar.markdown(f'## Hello *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
    
    elif selected == 'Generate RFP Response':
        generate_rfp_response()
        st.sidebar.markdown("""<div style="height: 15vh;"></div>""", unsafe_allow_html=True)
        st.sidebar.markdown(f'## Hello *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')
    
    elif selected == 'Query RFP Request':
        query_rfp_request()
        st.sidebar.markdown("""<div style="height: 15vh;"></div>""", unsafe_allow_html=True)
        st.sidebar.markdown(f'## Hello *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'sidebar')

elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.sidebar.warning('Please enter your username and password')
    st.write("# Welcome to RFP Builder! 👋")
    st.markdown(
        """
        Welcome to our Streamlit-powered Request for Proposal (RFP) Management System. 
        Our platform streamlines the RFP process, offering a seamless experience from 
        request QnA to response generation.

        **👈 Login and Select a demo from the sidebar** to see some examples
        of what RFP Builder can do!
        #### Key Features!
        - Chat and Query Functionality: Enable seamless chat and query from RFP request documents
          through built-in chat and query features, ensuring clarity and responsiveness throughout 
          the RFP lifecycle.
        - Response Generation: Simplify the creation of RFP responses by providing predefined 
          templates and customizable sections. MSPs can efficiently address each requirement 
          outlined in the RFP request, ensuring comprehensive and accurate responses.
        - Sectioned Response Creation: Our platform supports the creation of structured responses, 
          allowing MSPs to address each section and subsection of the RFP request systematically. 
          This ensures clarity and completeness in the delivered responses.
        """
    )
