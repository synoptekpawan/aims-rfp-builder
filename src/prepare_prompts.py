import sys
sys.path.append('D:\\synoptek-work-2023\\proj-AIMS\\synoptek-pawan\\aims-rfp-builder')

from prompts.all_prompts_v0 import *
from langchain_core.prompts import PromptTemplate


def prepare_prompts(sections, resp_template, llm_resp):
    prompts_dict={}
    prompts = prompts_()
    # print(resp_template)

    template="""
    Act as prompt engineer. You will be given with dictionary of prompts, a response template and additional info about section.
    Your task is to create a prompt for a section coming from user based on above two inputs.
    To achieve the task sucessfully perform following steps:
    - as you get the user section, extract its semantically matching content from response template in bullet points.
    - compare the user section and given dictionary of prompts semantically to get the matching reference prompt.
    - prepare a refined prompt using the extracted content and matching reference prompt.
    - the refined prompt must contain the options to consider external inputs, 
        if user section is table of contents add only list_of_section as variable for external inputs, 
        else it should add only extracted_text as variable for external inputs.
    - there are chances you can fail in extracting content or matching reference prompt based on user section.
    - so validate if extracted content and matching reference prompt are correct with respect to user section, if not redo above steps again.
    - in response give prepared refined prompt for each section, skip the other steps.
    - do not add any ai message at start end of response.

    user section:\n{section}

    additional info:\n{additional_info}

    dictionary of prompts:\n{prompts}

    response template:\n{resp_template}

    """
    prompt = PromptTemplate(
                            input_variables=["user section","additional info","dictionary of prompts","response template"],
                            template=template
                            )
    
    
    for section, additional_info in sections.items():
        section_prompt = prompt.format(
                                    section=section,
                                    additional_info=additional_info,
                                    prompts=prompts,
                                    resp_template=resp_template
                                    )
        # print(section_prompt)
        new_section_prompt = llm_resp.invoke(section_prompt)
        new_section_prompt_ = new_section_prompt.content
        prompts_dict[section] = new_section_prompt_

    return prompts_dict

        






        