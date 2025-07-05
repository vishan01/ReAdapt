import bs4
from langchain_community.document_loaders import WebBaseLoader
import asyncio 

def retrieve_data(page_url:str)->list[str]:
    """
    Retrieve the page data from the given url

    params:
        page_url: URL of the job description

    return:
        parsed data of the page
    """
    
    loader = WebBaseLoader(web_paths=[page_url])
    docs = []
    for doc in loader.load():
        docs.append(doc)

    doc = docs[0]
    return docs

