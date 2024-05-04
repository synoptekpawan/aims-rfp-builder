import streamlit as st

# @st.cache
def page_format():

    css = ''' 
    <style>
        [data-testid="stSidebar"]{
            min-width: 350px;
            max-width: 450px;
        }
        [data-testid="stSidebarContent"]{
            min-width: 300px;
            max-width: 400px;
        }
        
        [data-testid="block-container"]{
            min-width: 400px;
            max-width: 1250px;
        }
        
        button[data-baseweb="tab"] {
        font-size: 26px;
        }
                
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    # Page Title
    
