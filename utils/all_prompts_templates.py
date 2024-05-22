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
    human_template = f"""Create the {section} from extracted text as Synoptek is replying to RFP for {clientOrg}.
                        
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