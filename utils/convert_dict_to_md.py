import streamlit as st

# @st.cache
def dict_to_markdown(data):
    markdown_text = ""
    for key, value in data.items():
        markdown_text += f"**{key}:** {value}\n\n"
    return markdown_text