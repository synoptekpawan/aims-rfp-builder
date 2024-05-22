import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import streamlit as st
from utils.all_prompts_templates import *
import re
import json
import time
from langchain.chains import RetrievalQA
def generate_response(vector_store, llm_qa, llm_resp, prompts, clientOrg):

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_qa,
        retriever=vector_store.as_retriever()
    )
    
    start_time = time.time()
    business_objectives = qa_chain({"query":"extract all-phase business objectives from the provided document. Skip Pricing Model & Case Studies related documents."})
    koc = qa_chain({"query":"extract detailed key opportunities and challenges from the provided document. Skip Pricing Model & Case Studies related documents."})
    sow = qa_chain({"query":"extract detailed scope of work for all phases from the provided document. Skip Deliverables, Pricing Model & Case Studies related documents."})
    deliverables = qa_chain({"query":"extract detailed deliverables  for al phases from the provided document. Skip Scope of work, Pricing Model & Case Studies related documents."})
    
    st.sidebar.write("**Time taken to retrieve relevant documents in mins**")
    st.sidebar.write(round((time.time() - start_time)/60, 2))
    
    # sections = [section.lower() for section in sections]
    
    response = {}
    for section, prompt_template in prompts.items():
 
        if section == 'TABLE OF CONTENTS':
            prompt = prompt_builder_ai(prompt_template=prompt_template, section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    list_of_sections=prompts.keys(), clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
        
        else:
            prompt = prompt_builder_ai(prompt_template=prompt_template,section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text = '\n'.join([business_objectives['result'], koc['result'], 
                                    sow['result'], deliverables['result']]), clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content

    return response
