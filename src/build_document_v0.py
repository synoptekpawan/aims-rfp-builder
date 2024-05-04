import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from utils.all_prompts_templates import *
from prompts.all_prompts_v0 import *
import re
import json
import time
from langchain.chains import RetrievalQA

def generate_response(scope, clientOrg, sections, vector_store, llm_qa, llm_resp):

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
    
    sections = [section.lower() for section in sections]
    
    progress_text = "Generating Response. Please wait."
    my_bar = st.sidebar.progress(0, text=progress_text)
    
    response = {}
    
    for percent_complete, section  in enumerate(sections):
        time.sleep(0.01)
        my_bar.progress((percent_complete+1)/len(sections), text=progress_text)
            
        if section == 'executive summary':
            prompt = prompt_builder_ai(prompt_template=executive_summary_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=business_objectives['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
            
        elif section == 'understanding of business objectives':
            prompt = prompt_builder_ai(prompt_template=ubo_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=business_objectives['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
            
        elif section == 'key opportunities and challenges':
            prompt = prompt_builder_ai(prompt_template=koc_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=koc['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content

        elif section == 'scope of work':
            prompt = prompt_builder_ai(prompt_template=sow_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=sow['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content

        elif section == 'deliverables':
            prompt = prompt_builder_ai(prompt_template=deliverables_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=deliverables['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            resp_ = re.sub(r'\[doc \d+(\.\d+)* *- *\d+\]', '', response_.content)
            response[section] = resp_
            
        elif section == 'the synoptek approach':
            prompt = prompt_builder_ai(prompt_template=sa_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=deliverables['result'], clientOrg=clientOrg, section=section,
                    scope=scope
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
            
        elif section == 'transition plan':
            prompt = prompt_builder_ai(prompt_template=tp_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=sow['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
            
        elif section == 'execution timeline':
            prompt = prompt_builder_ai(prompt_template=tl_prompt_template(),section=section, clientOrg=clientOrg)
            # get a chat completion from the formatted messages
            response_ = llm_resp.invoke(
                prompt.format_prompt(
                    extracted_text=sow['result'], clientOrg=clientOrg, section=section,
                ).to_messages(),
                {"metadata": {"llm": "azure-openai",
                            "section":section}}
            )
            response[section] = response_.content
            
        elif section == 'synoptek team':
            response[section] = "User can add as per requirement"
            
        elif section == 'synoptek overview':
            synoptek_overview_txt = open(r"./static_texts/synoptek_overview.txt", "r", encoding="utf8")
            response[section] = synoptek_overview_txt.read()   
            
        elif section == 'synoptek\'s culture and approach to talent management': # X.	SYNOPTEK’S CULTURE AND APPROACH TO TALENT MANAGEMENT
            synoptek_talent_management_txt = open(r"./static_texts/synoptek_talent_management.txt", "r", encoding="utf8")    
            response[section] = synoptek_talent_management_txt.read()
            
        elif section == 'case studies':
            # Open the JSON file
            with open(r"./static_texts/case_studies.json") as f:
                data = json.load(f)
                result_string = ""

                for key, value in data["HealthCare"].items():
                    result_string += f"\n{key}\n{value[0]}\n"
            response[section] = result_string       
            
        elif section == 'quality security and compliance':
            quality_control_txt = open(r"./static_texts/quality_control.txt", "r", encoding="utf8")    
            response[section] = quality_control_txt.read()
            
        elif section == 'pricing model and pricing': 
            response[section] = "User can add as per requirement"

        elif section == 'assumptions and client responsibilities':
            assumptions_txt = open(r"./static_texts/assumptions.txt", "r", encoding="utf8")    
            response[section] = assumptions_txt.read()

        elif section == 'proposal appendix':
            response[section] = "User can add as per requirement"
            # response.append("NO")

        
    time.sleep(0.1)
    my_bar.empty()
    
    return response # static_texts\cover_letter.txt

    # return services



