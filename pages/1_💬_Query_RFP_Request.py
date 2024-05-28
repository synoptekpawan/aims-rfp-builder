## -------------------------------------------------
## load required packages
## -------------------------------------------------
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from datetime import date
today = date.today()
import time
from utils.process_file import process_file
from langchain_community.vectorstores import AzureSearch
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory, StreamlitChatMessageHistory
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.callbacks.manager import collect_runs
from langchain.schema.runnable import RunnableConfig
from langsmith import Client
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from streamlit_feedback import streamlit_feedback
import os
import csv
import random
from datetime import datetime
import logging

## -------------------------------------------------
## Configure logging
## -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

## -------------------------------------------------
## env vars and required vars
## -------------------------------------------------
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

vector_store_address: str = os.getenv("SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("SEARCH_KEY")

azure_openai_api_key: str = os.getenv("OPENAI_API_KEY_AZURE")
azure_endpoint: str = os.getenv("OPENAI_ENDPOINT_AZURE")

openai_api_key: str = os.getenv("OPENAI_API_KEY")

logger.info("Environment variables loaded")

## -------------------------------------------------
## set page config and options
## -------------------------------------------------
st.cache_data.clear()
st.cache_resource.clear()
logger.info("Cleared app cache")

st.set_page_config(page_title="Query RFP", page_icon="💬", layout="wide")
add_logo(r"./synoptek-new-removebg-3.png")

colored_header(
        label="💬 Query RFP", description="\n",
        color_name="violet-70",
    )

logger.info("Page configuration and options set up")

## -------------------------------------------------
## session state initialization
## -------------------------------------------------
if 'clientOrg' not in st.session_state:
    st.session_state['clientOrg'] = ''

if 'vector_store' not in st.session_state:
    st.session_state['vector_store'] = None

if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [
        {"role":"assistant", "content":"What you want to know from the RFP?"}
    ]

logger.info("Initialized session state")

## -------------------------------------------------
## rag function
## -------------------------------------------------
def rag_func(question: str, qa_chain) -> str:
    """
    Retrieve and generate an answer for the given question using the QA chain.

    Args:
        question (str): The question to be answered.

    Returns:
        str: The generated response for the given question.
    """
    try:
        resp = qa_chain({"query": question})
        return resp['result']
    except Exception as e:
        logger.exception("Error generating response: %s", e)

## -------------------------------------------------
## azure openai deployment and setup
## -------------------------------------------------
@st.cache_resource
def azure_openai_setup(azure_openai_api_key, azure_endpoint):
    """
    Set up Azure OpenAI models for QA and response generation.
    
    Args:
        azure_openai_api_key (str): API key for Azure OpenAI.
        azure_endpoint (str): Azure OpenAI endpoint.

    Returns:
        tuple: AzureChatOpenAI instances for QA and response generation.
    """
    try:
        logger.info("Setting up Azure OpenAI")
        deployment_gpt4_turbo = 'gpt-4-1106-preview'
        deployment_gpt4 = 'gpt-4'
        deployment_gpt35 = 'gpt-3.5-turbo-1106'
        deployemnt_gpt4_azure = 'gpt-4-aims'
        deployemnt_gpt35_azure = 'gpt-35-aims'

        llm_azure_qa = AzureChatOpenAI( 
            model_name=deployemnt_gpt4_azure,
            openai_api_key=azure_openai_api_key,
            azure_endpoint=azure_endpoint,
            openai_api_version="2024-04-01-preview",
            temperature=0,
            max_tokens=4000,
            model_kwargs={'seed':123}
            ) 

        llm_azure_resp = AzureChatOpenAI( 
            model_name=deployemnt_gpt35_azure,
            openai_api_key=azure_openai_api_key,
            azure_endpoint=azure_endpoint,
            openai_api_version="2024-04-01-preview",
            temperature=0,
            max_tokens=8000,
            model_kwargs={'seed':123}
            ) 

        logger.info("Azure OpenAI setup completed")
        return llm_azure_qa, llm_azure_resp
    except Exception as e:
        logger.exception("Error setting up Azure OpenAI: %s", e)
        st.error("Failed to set up Azure OpenAI. Please check the logs for details.")

azure_qa, azure_resp = azure_openai_setup(azure_openai_api_key, azure_endpoint)

# @st.cache_resource
# def openai_setup(openai_api_key):
#     """
#     Set up OpenAI models for QA and response generation.
    
#     Args:
#         openai_api_key (str): API key for OpenAI.

#     Returns:
#         tuple: ChatOpenAI instances for QA and response generation.
#     """
#     try:
#         logger.info("Setting up OpenAI")
#         deployment_gpt4_turbo = 'gpt-4-1106-preview'
#         deplyment_gpt4o = 'gpt-4o'
#         deployment_gpt4 = 'gpt-4'
#         deployment_gpt35 = 'gpt-3.5-turbo-1106'
#         deployemnt_gpt4_azure = 'gpt-4-aims'
#         deployemnt_gpt35_azure = 'gpt-35-aims'

#         llm_openai = ChatOpenAI(
#         model_name=deployment_gpt4,
#         openai_api_key=openai_api_key,
#         temperature=0,
#         max_tokens=4000,
#         model_kwargs={'seed':123}
#         )

#         logger.info("OpenAI setup completed")
#         return llm_openai
    
#     except Exception as e:
#         logger.exception("Error setting up OpenAI: %s", e)
#         st.error("Failed to set up OpenAI. Please check the logs for details.")
    
# llm_openai_ = openai_setup(openai_api_key)

## -------------------------------------------------
## azure cognitive search vector index setup
## -------------------------------------------------
@st.cache_resource
def azureai_search_setup(azure_endpoint, azure_openai_api_key):
    """
    Set up Azure AI search with embeddings.

    Args:
        azure_endpoint (str): Azure search endpoint.
        azure_openai_api_key (str): API key for Azure OpenAI.

    Returns:
        AzureOpenAIEmbeddings: Embeddings instance.
    """
    try:
        logger.info("Setting up Azure AI search")
        azure_deployment='embeddings-aims'
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=azure_deployment,
            openai_api_version="2024-04-01-preview",
            azure_endpoint=azure_endpoint,
            api_key=azure_openai_api_key,
        )
        logger.info("Azure AI search setup completed")
        return embeddings
    
    except Exception as e:
        logger.exception("Error setting up Azure AI search: %s", e)
        st.error("Failed to set up Azure AI search. Please check the logs for details.")

embedds = azureai_search_setup(azure_endpoint, azure_openai_api_key)

## -------------------------------------------------
## function for processing and uploading RFP request to Azure vector index
## -------------------------------------------------
@st.cache_resource
def create_vector_index(clientOrg, rfp, vector_store_address, vector_store_password):
    """
    Create a vector index for the given client organization and upload the RFP document.

    Args:
        clientOrg (str): Client organization name.
        rfp (UploadedFile): RFP document.
        vector_store_address (str): Vector store address.
        vector_store_password (str): Vector store password.

    Returns:
        AzureSearch: Vector store instance.
    """
    logger.info("Creating vector index for client organization: %s", clientOrg)
    index_name = "rfp-request-" + str(clientOrg).lower()
    try:
        vector_store_ = AzureSearch(
            azure_search_endpoint=vector_store_address,
            azure_search_key=vector_store_password,
            index_name=index_name,
            embedding_function=embedds.embed_query,
        )
        
        doc_count = vector_store_.client.get_document_count()
        logger.debug("Document count in vector store: %d", doc_count)

        if doc_count == 0:
            st.info("No document found in database for the given client.")
            if rfp is not None:
                logger.debug("Document provided, uploading to database.")
                st.info("Document attached. Uploading in database.")
                start_time = time.time()
                pages = process_file(file_name=rfp.name, file=rfp, bytes_data=rfp.read())
                # # from_tiktoken_encoder enables use to split on tokens rather than characters
                # recursive_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                # chunk_size=300, 
                # chunk_overlap=125
                # )

                # recursive_text_splitter_chunks = recursive_text_splitter.split_documents(pages)
                
                vector_store_.add_documents(documents=pages)
                time_taken = round((time.time() - start_time) / 60, 2)
                st.success(f"Document uploaded in {time_taken} mins.")
                logger.info("Document uploaded to vector store %s", index_name)
                #check if the file exists with path.exists()
                if os.path.exists(r'./temp/'+rfp.name):
                    os.remove(r'./temp/'+rfp.name)
                    logger.info('file deleted from temp folder')
                else:
                    logger.info("File does not exists in temp folder")
            else:
                st.warning("No document provided to upload.")
                logger.warning("No document provided for uploading to vector store %s", index_name)
        else:
            st.info("Document already exists in the database.")
            logger.warning("Document already exists in the vector store %s", index_name)

        return vector_store_
    except Exception as e:
        error_message = f"An error occurred while creating vector index for {clientOrg}: {e}"
        logger.exception(error_message)
        st.error(error_message)

## -------------------------------------------------
## upload rfp request
## -------------------------------------------------
with st.sidebar:
    
    st.session_state['clientOrg'] = st.text_input("**What is the client name?** 🚩")

    rfp = st.file_uploader("**Upload RFP request to database** 🚩")

    if st.session_state['clientOrg']:
        st.session_state['vector_store'] = create_vector_index(st.session_state['clientOrg'], rfp, vector_store_address, vector_store_password)
    else:
        st.warning("Add client name above")

## -------------------------------------------------
## setup memmory for app
## -------------------------------------------------

memory = ConversationBufferMemory(
    chat_memory=StreamlitChatMessageHistory(key="langchain_messages"), 
    return_messages=True, memory_key="chat_history")

if st.sidebar.button("Clear message history"):
    # st.sidebar.write("Clearing message history")
    memory.clear()
    st.session_state.trace_link = None
    st.session_state.run_id = None
    st.sidebar.write("Memory Cleared")


## -------------------------------------------------
## RFP Query app
## -------------------------------------------------

# qa_chain = ConversationalRetrievalChain.from_llm(
#         llm = llm_azure, 
#         memory = memory, 
#         retriever = vector_store.as_retriever(),
#         chain_type = "refine"
#     )
if st.session_state['vector_store']:
    vector_store = st.session_state['vector_store']
    qa_chain = RetrievalQA.from_chain_type(
            llm=azure_qa,
            retriever=vector_store.as_retriever()
        )

if "messages" in st.session_state.keys():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role":"user", "content":user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

input_dict = {"input": user_prompt}
try:
    with collect_runs() as cb:
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Loading....."):
                    try:
                        ai_response = rag_func(question=user_prompt, qa_chain=qa_chain)
                        st.write(ai_response)
                        logger.info("AI response generated successfully.")
                    except Exception as e:
                        logger.exception("Error generating AI response: %s", e)
                        st.error("Connection aborted. Please generate response template again")

            new_ai_message = {"role": "assistant", "content": ai_response}
            st.session_state.messages.append(new_ai_message)
            st.session_state.run_id = cb.traced_runs[0].id
            memory.save_context(input_dict, {"output": ai_response})
            logger.info("Session state updated and context saved successfully.")
except Exception as e:
    logger.exception("Error during the collection of runs or session state update: %s", e)
    st.error("Connection aborted. Please generate response template again")
        

# client = Client(api_url=os.getenv("LANGCHAIN_ENDPOINT"), api_key=os.getenv("LANGCHAIN_API_KEY"))

# feedback_option = "faces" # if st.toggle(label="`Thumbs` ⇄ `Faces`", value=False) else "thumbs"

# # if st.session_state.get("run_id"):
# #     feedback = streamlit_feedback(
# #         feedback_type=feedback_option,  # Apply the selected feedback style
# #         optional_text_label="[Optional] Please provide an explanation",  # Allow for additional comments
# #         key=f"feedback_{st.session_state.run_id}",
# #     )

# if st.session_state.get("run_id"):
#     run_id = st.session_state.run_id
#     feedback = streamlit_feedback(
#         feedback_type=feedback_option,
#         optional_text_label="[Optional] Please provide an explanation",
#         key=f"feedback_{run_id}",
#     )

#     # Define score mappings for both "thumbs" and "faces" feedback systems
#     score_mappings = {
#         "thumbs": {"👍": 1, "👎": 0},
#         "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
#     }

#     # Get the score mapping based on the selected feedback option
#     scores = score_mappings[feedback_option]

#     if feedback:
#         # Get the score from the selected feedback option's score mapping
#         score = scores.get(feedback["score"])

#         if score is not None:
#             # Formulate feedback type string incorporating the feedback option
#             # and score value
#             feedback_type_str = f"{feedback_option} {feedback['score']}"
#             try:
#                 feedback_record = client.create_feedback(
#                     run_id,
#                     feedback_type_str,
#                     score=score,
#                     comment=feedback.get("text"),
#                 )
#                 st.session_state.feedback = {
#                     "feedback_id": str(feedback_record.id),
#                     "score": score,
#                 }
#             except Exception as e:
#                 logger.exception("Error recording feedback: %s", e)
#                 st.error("Failed to record feedback. Please check the logs for details.")
            
#         else:
#             st.warning("Invalid feedback score.")

logger.info("-------------------------------------------------------------------")


