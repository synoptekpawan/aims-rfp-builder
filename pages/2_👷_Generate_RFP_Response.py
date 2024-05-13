## load required packages
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from langchain_community.vectorstores import AzureSearch
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_community.chat_models import AzureChatOpenAI, ChatOpenAI
import os
from utils.process_file import process_file
from src.build_document_v0 import generate_response
from docxtpl import DocxTemplate, RichText
from datetime import datetime
import jinja2
import io
import spacy
nlp = spacy.load("en_core_web_lg")
from docx import Document
from datetime import date
import time
import string
import random
today = date.today()

## langsmith setup
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

## function for processing, and uploading rfp request to azure vector index
@st.cache_resource
def create_vector_index(clientOrg, rfp):
    try:
        index_name = "rfp-request-"+str(clientOrg).lower()+"-"+str(today)
        vector_store_: AzureSearch = AzureSearch(
                azure_search_endpoint=vector_store_address,
                azure_search_key=vector_store_password,
                index_name=index_name,
                embedding_function=embeddings.embed_query,
            )
        
        if rfp is not None:
            # print(index_name)
            start_time = time.time()
            pages = process_file(file_name = rfp.name, file = rfp, bytes_data = rfp.read())
            doc_count = vector_store_.client.get_document_count()
            if doc_count == 0:
                vector_store_.add_documents(documents=pages)
            # add_pages_to_vs = add_docs_to_vectorStore(index_name,pages)
            # st.sidebar.write("Document upload finished, remove it to proceed with document generation")
            st.sidebar.write("**Time taken to upload a document in mins**")
            st.sidebar.write(round((time.time() - start_time)/60, 2))
            # print("running the vector_index")

        return vector_store_
    except:
        st.warning("add client name in side bar")

@st.cache_resource
def get_sections_for_rfp_response_template(_model, text):
    doc_text = _model(text)
    similarities = {}
    for option in options:
        doc_option = _model(option)
        similarity = doc_text.similarity(doc_option)
        similarities[option] = similarity*100
    print(similarities)
    
    similar_sections=[]
    for key, value in similarities.items():
        if value > 10:
            # print(f"{option}: {similarity:.4f}")
            similar_sections.append(key)
    # print(similar_sections)
    return similar_sections

## declare requried variables
global template
template=''
# vector=''

## set page config and options
st.set_page_config(layout="wide", page_title="Generate RFP Response", page_icon="👷")
add_logo(r"./synoptek-new-removebg-3.png")
colored_header(
        label="👷 Generate RFP Response", description="\n",
        color_name="violet-70",
    )

## azure openai deployment and setup
deployment_gpt4_turbo = 'gpt-4-1106-preview'
deployment_gpt4 = 'gpt-4'
deployment_gpt35 = 'gpt-3.5-turbo-1106'
deployemnt_gpt4_azure = 'gpt-4-aims'
deployemnt_gpt35_azure = 'gpt-35-aims'

llm_azure_qa = AzureChatOpenAI( 
    model_name=deployemnt_gpt4_azure,
    openai_api_key=os.getenv("OPENAI_API_KEY_AZURE"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT_AZURE"),
    openai_api_version="2023-12-01-preview",
    temperature=0,
    max_tokens=4000,
    model_kwargs={'seed':123}
    ) # 'topProbabilities':0

llm_azure_resp = AzureChatOpenAI( 
    model_name=deployemnt_gpt35_azure,
    openai_api_key=os.getenv("OPENAI_API_KEY_AZURE"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT_AZURE"),
    openai_api_version="2023-12-01-preview",
    temperature=0,
    max_tokens=8000,
    model_kwargs={'seed':123}
    ) # 'topProbabilities':0

## azure cognitive search vector index setup
vector_store_address: str = os.getenv("SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("SEARCH_KEY")

azure_deployment='embeddings-aims'
embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=azure_deployment,
    openai_api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT_AZURE"),
    api_key=os.getenv("OPENAI_API_KEY_AZURE"),
)

## upload rfp request
with st.sidebar:

    if 'clientOrg' not in st.session_state:
        st.session_state['clientOrg'] = ''

    clientOrg = st.text_input("**What is the client orgnisation name?** 🚩", 
                            key='clientOrg0', value=st.session_state['clientOrg'])

    st.session_state['clientOrg'] = clientOrg
    # clientOrg = st.text_input("**What is the client orgnisation name?** 🚩", key='clientOrg0')
    
    rfp = st.file_uploader("**Upload RFP Request Here!**")
   
    ## processing, and uploading rfp request to azure vector index
    vector_store = create_vector_index(clientOrg, rfp)

## streamlit app page
col1, col2 = st.columns([1.8,3])
with col1:
    with st.container(border=True):
        ## set up qa retrival
        qa_chain = RetrievalQA.from_chain_type(
        llm=llm_azure_qa,
        retriever=vector_store.as_retriever()
        )
        
        if st.button("Get Response Template"): # Fetch response template from Uploaded request- Retrieve response template.
            if clientOrg:
                st.info("Response template given in RFP request:")
                template = qa_chain({"query":"""Act as Client advisor, and try to extract certain information from this document - 1) All the sections or template of the response to be submitted as a response to this document by any company.
 
                                            I will try to reformat my instructions, i need to know the format of response document and to know that, it is required to get necessary sections, headers to be covered in the response. In order to generate those sections, we need you to act as retriever from document precisely only those sections which are required in the document and in correct order.
 
                                            still this list is very comprehensive, we need just those headers which are required in submittals or response document"""})
                st.write(template['result'])
            else:
                st.warning("add client name in side bar")

        # case_studies = st.multiselect("## **Select case studies from here**",
        #                               ['HealthCare','Finance'], key='caseStudies0')

with col2:
    with st.container(border=True):
        ## select sections
        select_all = st.checkbox('Select All Sections', key='selectAll')
        options = ['EXECUTIVE SUMMARY', 'UNDERSTANDING OF BUSINESS OBJECTIVES', 
                'KEY OPPORTUNITIES AND CHALLENGES','SCOPE OF WORK','DELIVERABLES','THE SYNOPTEK APPROACH','TRANSITION PLAN', 'EXECUTION TIMELINE',
                'SYNOPTEK TEAM','SYNOPTEK OVERVIEW','SYNOPTEK\'s CULTURE AND APPROACH TO TALENT MANAGEMENT',
                'CASE STUDIES','QUALITY SECURITY AND COMPLIANCE', 'PRICING MODEL AND PRICING',
                'ASSUMPTIONS AND CLIENT RESPONSIBILITIES','PROPOSAL APPENDIX']
        
        if select_all:
            sections = st.multiselect('**What sections to be included? 🚩**', 
                                      options, options, key='sections0')
        else:
            sections = st.multiselect('**What sections to be included? 🚩**', 
                                    options, key='sections0')
        if template:
            sections = get_sections_for_rfp_response_template(nlp, template['result'])

            if 'sections' not in st.session_state:
                st.session_state['sections'] = sections
            
            sections = st.multiselect('**Sections selected as per RFP response template? 🚩**', 
                                    options, default=st.session_state['sections'], key='sections1')
            
                      
        if sections:
            if len(sections) == 1:
                st.warning("You have selected only one section. To generate and download document select all sections.")
            # elif len(sections) < 16:
            #     st.warning("You have not selected all sections. To generate and download document select all sections.")

        print(sections)
        
        ## set title of doc
        if 'title' not in st.session_state:
            st.session_state['title'] = ''
    
        title = st.text_input("**What is the title of the document? 🚩**", 
                              key='title0',  value=st.session_state['title'])

        st.session_state['title'] = title
        print(title)
        
        ## set scope
        if 'scope' not in st.session_state:
            st.session_state['scope'] = ''

        scope = st.text_area("**Add information for synoptek approach 🚩**", 
                             key='approach0', height=400, value=st.session_state['scope'])

        st.session_state['scope'] = scope
        print(scope[0:10])
        
## set reference doc      
reference_docx = r"./reference_docs/template_doc.docx"
print(reference_docx)

## generate rfp response, create a word document
if scope and clientOrg and title and sections:
    if st.sidebar.button("Generate Document"): # len(sections) > 10 & len(sections) < 16
        print(scope)