import bs4
from langchain_community.document_loaders import WebBaseLoader
import asyncio 

def retrieve_data(page_url:str)->list[str]|tuple:
    """
    Retrieve the page data from the given url

    params:
        page_url: URL of the job description

    return:
        parsed data of the page
    """
    try:
        loader = WebBaseLoader(web_paths=[page_url])
        docs = []
        for doc in loader.load():
            docs.append(doc)

        doc = docs[0]
        return docs,None
    except Exception as e:
        return "WebLoader Error: Try providing different or Valid URL",e

