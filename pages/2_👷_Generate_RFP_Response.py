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
from docx import Document
from datetime import date
import time
import string
import random
today = date.today()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

# print("app_started")

st.set_page_config(layout="wide", page_title="Generate RFP Response", page_icon="👷")
add_logo(r"./synoptek-new-removebg-3.png")

colored_header(
        label="👷 Generate RFP Response", description="\n",
        color_name="violet-70",
    )

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

vector_store_address: str = os.getenv("SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("SEARCH_KEY")

# Option 2: Use AzureOpenAIEmbeddings with an Azure account
azure_deployment='embeddings-aims'
embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=azure_deployment,
    openai_api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT_AZURE"),
    api_key=os.getenv("OPENAI_API_KEY_AZURE"),
)

with st.sidebar:
    
    st.title('👷 Generate RFP Response') # 🤖
    clientOrg = st.text_input("**What is the client orgnisation name?** 🚩", key='clientOrg0')
    
    rfp = st.file_uploader("**Upload RFP Request Here!**")
    
@st.cache_resource
def create_vector_index(clientOrg, rfp):
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

vector_store = create_vector_index(clientOrg, rfp)

# vector_store = vars.get('vector_store')
col1, col2 = st.columns([1.8,3])
with col1:
    with st.container(border=True):
        # scope = st.text_area("**What is be the scope of RFP?**", key='approach0', height=300)
        sections = st.multiselect('## **What sections to be included? 🚩**',
                        ['EXECUTIVE SUMMARY', 'UNDERSTANDING OF BUSINESS OBJECTIVES', 
                        'KEY OPPORTUNITIES AND CHALLENGES','SCOPE OF WORK','DELIVERABLES','THE SYNOPTEK APPROACH','TRANSITION PLAN', 'EXECUTION TIMELINE',
                        'SYNOPTEK TEAM','SYNOPTEK OVERVIEW','SYNOPTEK\'s CULTURE AND APPROACH TO TALENT MANAGEMENT',
                        'CASE STUDIES','QUALITY SECURITY AND COMPLIANCE', 'PRICING MODEL AND PRICING',
                        'ASSUMPTIONS AND CLIENT RESPONSIBILITIES','PROPOSAL APPENDIX'],key='sections0')
        if sections:
            if len(sections) == 1:
                st.warning("You have selected only one section. To generate and download document select all sections.")
            elif len(sections) < 16:
                st.warning("You have not selected all sections. To generate and download document select all sections.")
        
        title = st.text_input("**What is the title of the document? 🚩**", key='title0')
        
        
        # case_studies = st.multiselect("## **Select case studies from here**",
        #                               ['HealthCare','Finance'], key='caseStudies0')
with col2:
    with st.container(border=True):
        # st.write("Welcome to tab2 col2")
        scope = st.text_area("**Add information for synoptek approach 🚩**", 
                             key='approach0', height=300)
        
        # pricing = st.text_area("**Add information for pricing**", key='pricing0', height=300)
        
# st.write(sections)
reference_docx = r"./reference_docs/template_doc.docx"
if scope and clientOrg and title and sections:
    if st.button("Generate Document"): # len(sections) > 10 & len(sections) < 16
        start_time = time.time()
        generated_resp = generate_response(scope,clientOrg, 
                                           sections,
                                           vector_store, llm_azure_qa, llm_azure_resp )
        st.write(generated_resp)
        tpl = DocxTemplate(reference_docx)
        # for i in range(len(sections)):
        try:
            context = {
                        "date_today": datetime.now().strftime(format='%B %d, %Y'),
                        "mspOrg":"SYNOPTEK LLC",
                        "clientOrg":clientOrg,
                        "title": title,
                        'executive_summary': generated_resp["executive summary"],
                        'understanding_of_business_objectives':generated_resp["understanding of business objectives"],
                        'key_opportunities_and_challenges':generated_resp["key opportunities and challenges"],
                        'scope_of_work':generated_resp["scope of work"],
                        'deliverables':generated_resp["deliverables"],
                        'the_synoptek_approach': generated_resp["the synoptek approach"],
                        'transition_plan': generated_resp["transition plan"],
                        'timeline_plan': generated_resp["execution timeline"],
                        'synoptek_team':generated_resp["synoptek team"],
                        'synoptek_overview':generated_resp["synoptek overview"],
                        'synoptek_culture_and_approach_to_talent_management':generated_resp["synoptek's culture and approach to talent management"],
                        'case_studies':generated_resp["case studies"],
                        'quality_service_compliance':generated_resp["quality security and compliance"],
                        'pricing_model':generated_resp["pricing model and pricing"],
                        'assumptions_and_client_responsibilities':generated_resp["assumptions and client responsibilities"],
                        'proposal_appendix':generated_resp["proposal appendix"]
                        }
            
            jinja_env = jinja2.Environment(autoescape=True)
            tpl.render(context, jinja_env)
            tpl.save(r'./output_files/'+clientOrg+'_rfp_template.docx')
            
            # code for enable document download
            doc = Document(r'./output_files/'+clientOrg+'_rfp_template.docx')
            bio = io.BytesIO()
            doc.save(bio)
            # st.sidebar.write("**Time taken to generate a document**")
            # st.sidebar.write(round(time.time() - start_time,2)/60)
            if doc:
                st.sidebar.write("**Time taken to generate a document in mins**")
                st.sidebar.write(round((time.time() - start_time)/60, 2))
                st.sidebar.download_button(
                    label="Click here to download",
                    data=bio.getvalue(),
                    file_name=clientOrg+'_rfp_template.docx',
                    mime="docx"
                )
        except:
            st.sidebar.error("To download generated document please select all sections.")

