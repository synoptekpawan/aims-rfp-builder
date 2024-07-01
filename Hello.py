#Imports
import streamlit as st
from streamlit_extras.app_logo import add_logo
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from streamlit_navigation_bar import st_navbar
from src.Generate_RFP_Response import generate_rfp_response
from src.Query_RFP_Request import query_rfp_request
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import logging
import pyotp
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Hello", page_icon="👋", layout="wide")
st.sidebar.image(r"./synoptek-new-removebg-3.png")

# Load config
connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
container_name = "rfp-storage"
blob_name = "config/config.yaml"
 
#BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
 
# blob content to stream
blob_client = container_client.get_blob_client(blob_name)
blob_data = blob_client.download_blob().readall()
 
# Load the YAML 
config = yaml.load(io.BytesIO(blob_data), Loader=yaml.SafeLoader)
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Initialize session state
def initialize_session_state():
    if 'otp_setup_complete' not in st.session_state:
        st.session_state['otp_setup_complete'] = False
    if 'otp_verified' not in st.session_state:
        st.session_state['otp_verified'] = False
    if 'show_qr_code' not in st.session_state:
        st.session_state['show_qr_code'] = False
    if "name" not in st.session_state:
        st.session_state.name = None
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Home"
    logger.info("Initialized session state")

initialize_session_state()

# Show the title when on the login page
if st.session_state["authentication_status"] is None:
    pass
    # st.title("RFP Response Builder")

# Authentication for App
with st.sidebar:
    name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    # Check for OTP Secret and Generate if Not Present
    user_data = config['credentials']['usernames'].get(username, {})
    otp_secret = user_data.get('otp_secret', "")

    if not otp_secret:
        otp_secret = pyotp.random_base32()
        config['credentials']['usernames'][username]['otp_secret'] = otp_secret
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
        st.session_state['otp_setup_complete'] = False
        st.session_state['show_qr_code'] = True
        logger.info("Generated new OTP secret and set show_qr_code to True")
    else:
        st.session_state['otp_setup_complete'] = True

    # Ensure OTP secret is properly handled
    if otp_secret:
        totp = pyotp.TOTP(otp_secret)

        if not st.session_state['otp_verified']:
            # Display QR code for OTP setup only if not completed
            if st.session_state['show_qr_code']:
                with st.container(border=True):
                    st.title("Welcome to RFP Builder! 👋")
                logger.info("Displaying QR code for initial OTP setup")
                otp_uri = totp.provisioning_uri(name=user_data.get('email', ''), issuer_name="RFP Response Builder")
                qr = qrcode.make(otp_uri)
                qr = qr.resize((200, 200))  # Resize the QR code to a smaller size

                st.image(qr, caption="Scan this QR code with your authenticator app")

            # Prompt for OTP Verification
            otp_input = st.text_input("Enter the OTP from your authenticator app", type="password")
            verify_button_clicked = st.button("Verify OTP")

            if verify_button_clicked:
                if totp.verify(otp_input):
                    st.session_state['otp_verified'] = True
                    st.session_state['show_qr_code'] = False
                    st.experimental_rerun()
                else:
                    st.error("Invalid OTP. Please try again.")
        else:
            # Navigation and Main Content ok..
            styles = {
                "span": {
                    "border-radius": "0.1rem",
                    "color": "rgb(49, 51, 63)",
                    "margin": "0 0.125rem",
                    "padding": "0.400rem 0.400rem",
                },
                "active": {
                    "background-color": "rgba(255, 255, 255, 0.25)",
                },
            }

            selected = st_navbar(["Home", "Generate RFP Response", "Query RFP Request"],
                                selected=st.session_state.selected_option, styles=styles)

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
                    -   Chat and Query Functionality: Enable seamless chat and query from rfp request documents 
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
                st.session_state.selected_option = 'Home'
            elif selected == 'Generate RFP Response':
                generate_rfp_response()
                st.session_state.selected_option = 'Generate RFP Response'

            elif selected == 'Query RFP Request':
                query_rfp_request()
                st.session_state.selected_option = 'Query RFP Request'
                # st.experimental_rerun()
            else:
                pass

            st.sidebar.markdown("""<div style="height: 8vh;"></div>""", unsafe_allow_html=True)
            st.sidebar.markdown(f'## Hello, *{st.session_state["name"]}*')
            if st.sidebar.button("Logout", key="logout_button"):
                authenticator.logout('Logout', 'sidebar')
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()

elif st.session_state["authentication_status"] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
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
        -   Chat and Query Functionality: Enable seamless chat and query from rfp request documents
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