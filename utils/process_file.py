import streamlit as st
from collections import namedtuple
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, UnstructuredExcelLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyMuPDFLoader
from PyPDF2 import PdfReader
from tempfile import NamedTemporaryFile
import os
import pandas as pd

# @st.cache
def process_file(file_name, file, bytes_data):
    """
    This function helps in processing uploaded file:
    Input: file_name, file_path
    Output: list of prcocessed documents
    """
    # Declaring namedtuple()
    Document = namedtuple('Document', 'page_content metadata')
    if '.pdf' in file_name:
        # read pdf file
        with open(file_name, mode='wb') as w:
            w.write(file.getvalue())
        loader = PyMuPDFLoader(file_name)
        pages_ = loader.load()
        # pages_ = [page.page_content.lower() for page in pages_]
        # # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        # pages_ = [page.replace("’","'") for page in pages_]
        # pages_ = [page.replace("○","-") for page in pages_]
        # pages_ = [page.replace("•","-") for page in pages_]
        # pages_ = [page.replace("●","-") for page in pages_]
        # pages_ = [page.replace("\n", " ") for page in pages_]
        # pages_ = [page.lstrip().rstrip() for page in pages_]
        # pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]
        return pages_
    
    if ".xlsx" in file_name:
        with open(file.name, mode='wb') as w:
            w.write(file.getvalue())
        loader = UnstructuredExcelLoader(file.name, mode="paged")
        pages_ = loader.load()
        pages_ = [page.lower() for page in pages_]
        # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        pages_ = [page.replace("’","'") for page in pages_]
        pages_ = [page.replace("○","-") for page in pages_]
        pages_ = [page.replace("•","-") for page in pages_]
        pages_ = [page.replace("●","-") for page in pages_]
        pages_ = [page.replace("\n", " ") for page in pages_]
        pages_ = [page.lstrip().rstrip() for page in pages_]
        pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]

        return pages_
    
    if ".docx" in file_name:
        with open(file.name, mode='wb') as w:
            w.write(file.getvalue())
        loader = Docx2txtLoader(file.name)
        pages_ = loader.load()
        pages_ = [page.page_content.lower() for page in pages_]
        # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        pages_ = [page.replace("’","'") for page in pages_]
        pages_ = [page.replace("○","-") for page in pages_]
        pages_ = [page.replace("•","-") for page in pages_]
        pages_ = [page.replace("●","-") for page in pages_]
        pages_ = [page.replace("\n", " ") for page in pages_]
        pages_ = [page.lstrip().rstrip() for page in pages_]
        pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]

        return pages_
    
    if ".txt" in file_name:
        with open(file.name, mode='wb') as w:
            w.write(file.getvalue())
        loader = TextLoader(file.name, encoding = 'UTF-8')
        pages_ = loader.load()
        pages_ = [page.page_content.lower() for page in pages_]
        # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        pages_ = [page.replace("’","'") for page in pages_]
        pages_ = [page.replace("○","-") for page in pages_]
        pages_ = [page.replace("•","-") for page in pages_]
        pages_ = [page.replace("●","-") for page in pages_]
        pages_ = [page.replace("\n", " ") for page in pages_]
        pages_ = [page.lstrip().rstrip() for page in pages_]
        pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]

        return pages_
    
    if ".md" in file_name:
        with open(file.name, mode='wb') as w:
            w.write(file.getvalue())
        loader = TextLoader(file.name)
        pages_ = loader.load()
        pages_ = [page.page_content.lower() for page in pages_]
        # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        pages_ = [page.replace("’","'") for page in pages_]
        pages_ = [page.replace("○","-") for page in pages_]
        pages_ = [page.replace("•","-") for page in pages_]
        pages_ = [page.replace("●","-") for page in pages_]
        pages_ = [page.replace("\n", " ") for page in pages_]
        pages_ = [page.lstrip().rstrip() for page in pages_]
        pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]

        return pages_
    
    if ".csv" in file_name:
        with open(file.name, mode='wb') as w:
            w.write(file.getvalue())
        loader = CSVLoader(file.name)
        pages_ = loader.load()
        pages_ = [page.page_content.lower() for page in pages_]
        # pages_ = [page.replace("aetion, inc. - confidential","") for page in pages_]
        pages_ = [page.replace("’","'") for page in pages_]
        pages_ = [page.replace("ï»¿","'") for page in pages_]
        pages_ = [page.replace("○","-") for page in pages_]
        pages_ = [page.replace("•","-") for page in pages_]
        pages_ = [page.replace("●","-") for page in pages_]
        pages_ = [page.replace("\n", " ") for page in pages_]
        pages_ = [page.lstrip().rstrip() for page in pages_]
        pages_ = [Document(page,{'source':file_name, 'page':idx}) for idx, page in enumerate(pages_)]

        return pages_
        

        
    