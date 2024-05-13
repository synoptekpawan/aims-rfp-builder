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

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

st.set_page_config(page_title="Query RFP", page_icon="💬", layout="wide")
add_logo(r"./synoptek-new-removebg-3.png")

colored_header(
        label="💬 Query RFP", description="\n",
        color_name="violet-70",
    )

# index_name = st.sidebar.text_input("**Add index name for the doc**")
# index_name = "rfp-request-marta-"

deployment_gpt4_turbo = 'gpt-4-1106-preview'
deployment_gpt4 = 'gpt-4'
deployment_gpt35 = 'gpt-3.5-turbo-1106'
deployemnt_gpt4_azure = 'gpt-4-aims'
deployemnt_gpt35_azure = 'gpt-35-aims'

llm_azure = AzureChatOpenAI( 
    model_name=deployemnt_gpt4_azure,
    openai_api_key=os.getenv("OPENAI_API_KEY_AZURE"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT_AZURE"),
    openai_api_version="2023-12-01-preview",
    temperature=0.1,
    max_tokens=1000,
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
    # st.title('💬 Query RFP Request') # 🤖
    clientOrg = st.text_input("**What is the client orgnisation name?**", key='clientOrg0')
    index_name = "rfp-request-"+str(clientOrg).lower()+"-"+str(today)
    vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=vector_store_address,
            azure_search_key=vector_store_password,
            index_name=index_name,
            embedding_function=embeddings.embed_query,
        )
    rfp = st.file_uploader("**Upload RFP Request Here!**")
    if rfp is not None:
        # print(index_name)
        start_time = time.time()
        pages = process_file(file_name = rfp.name, file = rfp, bytes_data = rfp.read())
        doc_count = vector_store.client.get_document_count()
        if doc_count == 0:
            vector_store.add_documents(documents=pages)
        # add_pages_to_vs = add_docs_to_vectorStore(index_name,pages)
        st.sidebar.write("Document upload finished, remove it to proceed with query")
        st.sidebar.write("**Time taken to upload a document in mins**")
        st.sidebar.write(round((time.time() - start_time)/60, 2))

memory = ConversationBufferMemory(
    chat_memory=StreamlitChatMessageHistory(key="langchain_messages"), 
    return_messages=True, memory_key="chat_history")

if st.sidebar.button("Clear message history"):
    # st.sidebar.write("Clearing message history")
    memory.clear()
    st.session_state.trace_link = None
    st.session_state.run_id = None
    st.sidebar.write("Memory Cleared")

# qa_chain = ConversationalRetrievalChain.from_llm(
#         llm = llm_azure, 
#         memory = memory, 
#         retriever = vector_store.as_retriever(),
#         chain_type = "refine"
#     )

qa_chain = RetrievalQA.from_chain_type(
        llm=llm_azure,
        retriever=vector_store.as_retriever()
    )

def rag_func(question:str) -> str:
    resp = qa_chain({"query":question})
    # return resp.get("answer")
    return resp['result']

if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [
        {"role":"assistant", "content":"What you want to know from the RFP?"}
    ]

if "messages" in st.session_state.keys():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role":"user", "content":user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

input_dict = {"input":user_prompt}
with collect_runs() as cb:
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading....."):
                ai_response = rag_func(user_prompt)
                st.write(ai_response)
        new_ai_message = {"role":"assistant", "content":ai_response}
        st.session_state.messages.append(new_ai_message)
        st.session_state.run_id = cb.traced_runs[0].id
        memory.save_context(input_dict, {"output": ai_response})
        

client = Client(api_url=os.getenv("LANGCHAIN_ENDPOINT"), api_key=os.getenv("LANGCHAIN_API_KEY"))

feedback_option = "faces" # if st.toggle(label="`Thumbs` ⇄ `Faces`", value=False) else "thumbs"

# if st.session_state.get("run_id"):
#     feedback = streamlit_feedback(
#         feedback_type=feedback_option,  # Apply the selected feedback style
#         optional_text_label="[Optional] Please provide an explanation",  # Allow for additional comments
#         key=f"feedback_{st.session_state.run_id}",
#     )

if st.session_state.get("run_id"):
    run_id = st.session_state.run_id
    feedback = streamlit_feedback(
        feedback_type=feedback_option,
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{run_id}",
    )

    # Define score mappings for both "thumbs" and "faces" feedback systems
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }

    # Get the score mapping based on the selected feedback option
    scores = score_mappings[feedback_option]

    if feedback:
        # Get the score from the selected feedback option's score mapping
        score = scores.get(feedback["score"])

        if score is not None:
            # Formulate feedback type string incorporating the feedback option
            # and score value
            feedback_type_str = f"{feedback_option} {feedback['score']}"

            # Record the feedback with the formulated feedback type string
            # and optional comment
            feedback_record = client.create_feedback(
                run_id,
                feedback_type_str,
                score=score,
                comment=feedback.get("text"),
            )
            st.session_state.feedback = {
                "feedback_id": str(feedback_record.id),
                "score": score,
            }

            # memory.save_context(input_dict, {"feedback": st.session_state.feedback})
            
        else:
            st.warning("Invalid feedback score.")


