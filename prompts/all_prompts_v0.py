import streamlit as st

# @st.cache_data
def sectionIndex():
    prompt = """
            As an AI assistant, your task is to construct an index page.
            Add sections and subsections 
            This index should serve as a navigational guide, enabling easy access to each major section and their respective subsections as follows:
                -EXECUTIVE SUMMARY AND OVERVIEW
                -SCOPE OF WORK
                -TRANSITION PLAN AND APPROACH
                -ROLES AND RESPONSIBILITIES
                -CLIENT RESPONSIBILITIES
                -TECH STACK & SERVICES
                -COST AND TIMELINE
                -TERMS AND CONDITIONS
                -ASSUMPTIONS
            Ensure the document is crafted in proper markdown format, reflecting the section title and subsections accurately. It should be direct and free from any external citations or documents; any discovered should be eliminated. Additionally, avoid incorporating unnecessary text simply to fill space. Any found should be omitted.
            Do not add any Note section additionally.
            """
    return prompt

# @st.cache_data
def cover_letter_prompt_template():
    prompt = """
                You are tasked with enhancing a provided text for a technical cover letter without using any headings or numbered points in the response. 
                Each section of the cover letter should be elaborated upon in markdown format with up to 8000 tokens per point, and the response should begin directly with the content, not an AI-generated introduction. 
                The sections to address in the cover letter are:
                -   Expressing appreciation and introducing the topic.
                -   Demonstrating an understanding of the needs of the client.
                -   Highlighting the unique qualifications and differentiators of Synoptek.
                -   Detailing the specific services and solutions offered.
                -   Discussing future opportunities for collaboration.
                -   Concluding the letter with closing remarks.
                ---
                Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def executive_summary_prompt_template():
    prompt = """
            You are tasked with creating a technical executive summary based on provided text. 
            The response should be in markdown format and begin directly with the content, without any headings or numbered points. 
            The executive summary should be detailed using up to 8000 tokens per section. 
            Focus on the following aspects:

            -   Overview of the proposed partnership.
            -   Outline of the unique value proposition offered by Synoptek.
            -   Projection of estimated costs, potential incentives, and financial benefits.
            -   Summary of the ongoing support and resources Synoptek will provide.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def background_prompt_template():
    prompt = """
            You are tasked with developing a technical background from the provided text. 
            The response should be formatted in markdown and begin directly with the content, 
            avoiding any AI introductory notes or concluding remarks. Elaborate the content using up to 8000 tokens, 
            ensuring a comprehensive and detailed presentation of the background information.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def ubo_prompt_template():
    prompt = """
            You are tasked with creating a technical business objective from provided text. 
            Format the response in markdown, starting directly with the content and without AI introductions 
            or conclusions. Elaborate on the essential elements using up to 8000 tokens. 
            Focus on detailing the innovative program features that will meet business objectives 
            and highlighting the capabilities that ensure future-proofing by Synoptek.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache
def koc_prompt_template():
    prompt = """
            You are tasked with detailing the technical opportunities and challenges derived from provided text, 
            formatted in markdown. Start directly with the content without AI introductions or conclusions at the end of response, 
            and elaborate using up to 8000 tokens on:

            -   Client specific and common challenges
            -   Strategic goals of partnerships, particularly focusing on client benefits and objectives.
            -   Critical success factors essential for the effectiveness of global teams.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def sow_prompt_template():
    prompt = """
            You are tasked with creating a technical scope of work based on provided text, 
            formatted in markdown without using an AI introduction or concluding statements. 
            Begin directly with the content and detail each key element comprehensively using 
            up to 8000 tokens. Focus on outlining the specific tasks.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def deliverables_prompt_template():
    prompt = """
            You are tasked with describing the technical deliverables derived from provided text. 
            This should be formatted in markdown, starting directly with the content and without 
            concluding statements. Elaborate on each deliverable using up to 8000 tokens to detail 
            the expected outputs, project milestones, documentation, and any specific client requirements 
            that need to be met.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def sa_prompt_template():
    prompt = """
            You are tasked with outlining a technical approach based on the extracted text, 
            under the theme "Envision, Transform, Evolve." This response should be formatted in 
            markdown and directly delve into the content. Describe the detailed steps of delivery 
            for the objectives and services requested, using up to 8000 tokens to explain each phase:
            -   Envision details the initial planning and objectives setting.
            -   Transform describes the implementation processes and methodologies.
            -   Evolve covers the continuous improvement and future enhancements of the services.
            ---
            Here is the example of extracted text:\n{extracted_text}
            ---
            Here is additional information:\n{scope}
            """
    return prompt

# @st.cache
def tp_prompt_template():
    prompt = """
            You are tasked with developing a technical transition plan based on the provided text. 
            Begin directly with the content formatted in markdown. Elaborate on the essential components of 
            the transition process using up to 8000 tokens to detail:
            -   An introduction to the transition plan, setting the stage for the activities and approach.
            -   A description of the transition approach, outlining the strategies and methodologies to be employed.
            -   A rundown of key transition activities, specifying the main tasks and milestones critical to the success of the transition.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache
def tl_prompt_template():
    prompt = """
            You are tasked with crafting a technical timeline plan table based on the provided text. 
            Begin directly with the content formatted in markdown. Detail each phase and milestone in 
            the project's timeline using up to 6000 tokens, ensuring to clearly outline the expected 
            start and end dates, key deliverables, and responsible parties for each stage of the project.
            - Introduction to Timeline
            - Detailed tabular Timeline
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

def so_prompt_template():
    prompt = """
            You are a synoptek overview writer that creates technical synoptek overview as per provided domain, servies and from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical synoptek overview should elaborate using up to 6000 tokens for each point in response.
            ---
            Here is the example of extracted text:\n{extracted_text}
            ---
            Here is the example of domain :\n{domain}
            
            """
    return prompt

def sc_prompt_template():
    prompt = """
            You are a synoptek\'s culture and approach to talent management writer that creates synoptek\'s culture and approach to talent management as per provided domain, servies and from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The Synoptek\'s culture and approach to talent management should elaborate using up to 6000 tokens for each point in response.
            ---
            Here is the example of extracted text:\n{extracted_text}
            ---
            Here is the example of domain:\n{domain}
            """
    return prompt

def pm_prompt_template():
    prompt = """
            You are a pricing model writer that creates pricing model as per provided domain, servies and from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The pricing model should elaborate using up to 6000 tokens for each point in response
            ---
            Here is the example of extracted text:\n{extracted_text}
            ---
            Here is the example of pricing model:\n{pricing_model}
            """
    return prompt
