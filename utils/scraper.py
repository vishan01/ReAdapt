import bs4
from langchain_community.document_loaders import WebBaseLoader

def retrieve_data(page_url:str)->list[str]:
    """
    Retrieve the page data from the given url

    params:
        page_url: URL of the job description

    return:
        Parsed_data

    """
    loader = WebBaseLoader(web_paths=[page_url])
    docs = []
    for doc in loader.load():
        docs.append(doc.page_content)

    return docs
    