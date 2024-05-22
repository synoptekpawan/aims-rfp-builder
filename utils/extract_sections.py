from langchain import PromptTemplate

def extract_sections(response_template):

    template = """
                -Create a Section headers from the given text which includes contents of the technical proposal or vendor response specifications or response requirements.
                -Exclude points related to additional information, attachment related content, evaluation criteria, etc.
                -There are chances you can miss information.
                -So validate if information is complete, if not redo above steps again till get all sectional headers.
                -Provide a python list of these section headers in output"

    Context: {response_template}

    Response: """

    prompt = PromptTemplate(
                            input_variables=["context"],
                            template=template
                            )
    final_prompt = prompt.format(
                                response_template=response_template
                                )

    return final_prompt