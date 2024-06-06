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
                You are a cover letter writer that update the extracted text\n
                Do not start the response by a message from ai and "Dear <Header>". Do not put point headings in response.
                Start by section name only. Give markdown response. No need of adding conclusion in response.
                The technical cover letter should elaborate using up to 6000 tokens for each point in response:\n
                - Introduction and Gratitude
                - Understanding of client Needs
                - Synoptek's Qualifications and Differentiators
                - Specific Services and Solutions Offered
                - Future Opportunities
                - Closing Remarks
                ---
                Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def executive_summary_prompt_template():
    prompt = """
            You are a executive summary writer that creates techincal executive summary from the extracted text.\n
            Do not start the response by a message from ai. Do not put point headings in response. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical executive summary should elaborate using up to 6000 tokens for each point in response:\n
             - Introduction
             - Partnership Proposal
             - Synoptek's Credentials and Experience
             - Services Offered and Benefits of Partnership
             - Future Development Opportunities
             - Value Proposition
             - Cost Estimates and Incentives
             - Synoptek's Support
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def background_prompt_template():
    prompt = """
            You are a background writer that creates techincal background from the extracted text.\n
            Do not start the response by a message from ai. Do not put point headings in response. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical background should elaborate using up to 6000 tokens for each point in response.
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache_data
def ubo_prompt_template():
    prompt = """
            You are a business objective writer that creates techincal business objective from the extracted text.\n
            Do not start the response by a message from ai. Do not put point headings in response. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The techincal business objective should elaborate using up to 6000 tokens for each point in response:\n
            - Understanding of Business Objectives
            - Synoptek's Proposal and Solutions
            - Program Features to Meet Business Objectives
            - Capabilities and Future-proofing by Synoptek
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache
def koc_prompt_template():
    prompt = """
            You are a opportunities and challenges writer that creates techincal opportunities and challenges from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The techincal opportunities and challenges should elaborate using up to 6000 tokens for each point in response:\n
            - Strategic Partnership Goals
            - Specific Challenges
            - Common Challenges in Global Engineering Models
            - Synoptek's Experience and Approach
            - Critical Success Factors for Global Teams
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def sow_prompt_template():
    prompt = """
            You are a scope of work writer that creates technical scope of work from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical scope of work should elaborate using up to 6000 tokens for each point in response:\n
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def deliverables_prompt_template():
    prompt = """
            You are a deliverables writer that creates technical deliverables from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical deliverables should elaborate using up to 6000 tokens for each point in response:\n
            ---
            Here is the example of extracted text:\n{extracted_text}
            """

    return prompt

# @st.cache
def sa_prompt_template():
    prompt = """
            You are a approach writer that creates techincal approach from the extracted text.\n
            The technical approach have a Envision, Transform, Evolve theme.
            It elaborate the detailed steps of delivery for objectives and services requested in extracted text using up to 6000 tokens for each point in response:\n
            Do not start the response by a message from ai. Do not put point headings in response. No need of adding conclusion in response. Start by section name only. Give markdown response.
            ---
            Here is the example of extracted text:\n{extracted_text}
            ---
            Here is additional information:\n{scope}
            """
    return prompt

# @st.cache
def tp_prompt_template():
    prompt = """
            You are a transition plan writer that creates techincal transition plan from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical transition plan should elaborate using up to 6000 tokens for each point in response:
            - Introduction to Transition Plan
            - Transition Approach
            - Key Transition Activities
            ---
            Here is the example of extracted text:\n{extracted_text}
            """
    return prompt

# @st.cache
def tl_prompt_template():
    prompt = """
            You are a timeline plan table writer that creates techincal timeline plan table from the extracted text.\n
            Do not start the response by a message from ai. No need of adding conclusion in response. Start by section name only. Give markdown response.
            The technical timeline plan table should elaborate using up to 6000 tokens for each point in response:
            - Introduction to Timeline
            - Key Activities
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
