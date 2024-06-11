import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import streamlit as st
from utils.all_prompts_templates import *
from prompts.all_prompts_v1 import *
import re
import json
import time
from langchain.chains import RetrievalQA

def process_case_studies(case_studies):
    try:
        # response = {}
        with open(r"./static_texts/case_studies.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            result_string = ""
            case_study_count = 1

            for selected_case_study in case_studies:
                if selected_case_study in data:
                    result_string += f"\nCase Study {case_study_count}: {selected_case_study}\n"
                    for key, value in data[selected_case_study].items():
                        result_string += f"\n{key}\n{value[0] if isinstance(value, list) else value}\n"
                    case_study_count += 1  # Increment the counter after processing a case study
                else:
                    result_string += f"\nSelected case study {selected_case_study} not found.\n"

            # response['case studies'] = result_string
        return result_string
        
        # return response
    except Exception as e:
        print(f"Error: {e}")
        return {}

# @st.cache_resource() #suppress_st_warning=True, allow_output_mutation=True
def generate_response(vector_store, llm_qa, llm_resp, prompts, clientOrg, case_studies):

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_qa,
        retriever=vector_store.as_retriever()
    )
    
    start_time = time.time()
    business_objectives = qa_chain({"query":"extract all-phase business objectives from the provided document. Skip Pricing Model & Case Studies related documents."})
    koc = qa_chain({"query":"extract detailed key opportunities and challenges from the provided document. Skip Pricing Model & Case Studies related documents."})
    sow = qa_chain({"query":"extract detailed scope of work for all phases from the provided document. Skip Deliverables, Pricing Model & Case Studies related documents."})
    deliverables = qa_chain({"query":"extract detailed deliverables  for al phases from the provided document. Skip Scope of work, Pricing Model & Case Studies related documents."})
    domain = qa_chain({"query":"Extract industry domain with description from the provided document."})
    
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

        elif section == 'SYNOPTEK OVERVIEW':
            synoptek_overview_txt = open(r"./static_texts/synoptek_overview.txt", "r", encoding="utf8")
            # prompt = prompt_builder_static(prompt_template=so_prompt_template(),section=section, clientOrg=clientOrg)
            # # get a chat completion from the formatted messages
            # response_ = llm_resp.invoke(
            #     prompt.format_prompt(
            #         extracted_text=synoptek_overview_txt.read(), clientOrg=clientOrg, 
            #         section=section, domain=domain['result']
            #     ).to_messages(),
            #     {"metadata": {"llm": "azure-openai",
            #                 "section":section}}
            # )
            # response[section] = response_.content
            response[section] = synoptek_overview_txt.read()

        elif section == 'SYNOPTEK\'s CULTURE AND APPROACH TO TALENT MANAGEMENT':
            synoptek_talent_management_txt = open(r"./static_texts/synoptek_talent_management.txt", "r", encoding="utf8")    
            # prompt = prompt_builder_static(prompt_template=sc_prompt_template(),section=section, clientOrg=clientOrg)
            # # get a chat completion from the formatted messages
            # response_ = llm_resp.invoke(
            #     prompt.format_prompt(
            #         extracted_text=synoptek_talent_management_txt.read(), clientOrg=clientOrg, 
            #         section=section, domain=domain['result']
            #     ).to_messages(),
            #     {"metadata": {"llm": "azure-openai",
            #                 "section":section}}
            # )
            # response[section] = response_.content
            response[section] = synoptek_talent_management_txt.read()

        elif section == 'CASE STUDIES':
            # # Open the JSON file
            # with open(r"./static_texts/case_studies.json") as f:
            #     data = json.load(f)
            #     result_string = ""

            #     for key, value in data["HealthCare"].items():
            #         result_string += f"\n{key}\n{value[0]}\n"
            # response[section] = result_string
            response[section] = process_case_studies(case_studies)

        elif section == 'QUALITY SECURITY AND COMPLIANCE':
            quality_control_txt = open(r"./static_texts/quality_control.txt", "r", encoding="utf8")    
            response[section] = quality_control_txt.read()

        elif section == 'ASSUMPTIONS AND CLIENT RESPONSIBILITIES':
            assumptions_txt = open(r"./static_texts/assumptions.txt", "r", encoding="utf8")    
            response[section] = assumptions_txt.read()
        
        else:
            prompt = prompt_builder_ai(prompt_template=prompt_template,section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text = '\n'.join([business_objectives['result'], koc['result'], 
                                    sow['result'], deliverables['result']]), clientOrg=clientOrg, 
                                    section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content

    return response
