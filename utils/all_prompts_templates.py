from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
# The {section} document should outline following points:
# {points}

# @st.cache
def prompt_builder_ai(section, clientOrg, prompt_template):
    prompt_template = prompt_template

    system_message_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
    # human_template = f"""Create {section} document for {clientOrg}.
                        
    #                     """
    human_template = f"""Act as business analyst. Your task is to create the content for {section} from extracted text as if Synoptek is replying to RFP for {clientOrg}.
                        To create a content for a user section perform following steps:
                        - check what is the user section.
                        - you are provided with documents of business objectives, scope of work, opportunities and challenges, and deliverables.
                        - check which document is relevant for which section, and use that document accordingly in that section as extracted text.
                        - if you fail in finding relevent document as per section, recheck the above step again.
                        - skip any AI message at start or end of the generated content.
                        - finally while creating content use more than 8000 tokens, to create a elaborated content.
                        
                        """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    return prompt

def prompt_builder_static(section, clientOrg, prompt_template):
    prompt_template = prompt_template

    system_message_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
    # human_template = f"""Create {section} document for {clientOrg}.
                        
    #                     """
    human_template = f"""Create the {section} from extracted text as Synoptek is replying to RFP for {clientOrg}
                        based on objectives and services requested.
                        
                        """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    return prompt