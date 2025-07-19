from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class JobInfo(BaseModel):
    job_title: str
    job_skills: str
    job_description: str

def parse_job_posting(job_posting_text: str) -> JobInfo|tuple:
    """
    Parses the job posting and extracts the required informations such as:
    skills, Title, Description

    params:
    job_posting_text: Extracted Job Role Description Text

    return:
    JobInfo: Json formated text regarding the job
    
    """
    parser = JsonOutputParser(pydantic_object=JobInfo)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate.from_template("""
    Extract structured job information in JSON format using the following schema.

    {format_instructions}

    Job Posting:
    {job_posting}
    """)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0)
    chain = prompt | llm | parser
    try:
        parsed_text=chain.invoke({
            "job_posting": job_posting_text,
            "format_instructions": format_instructions
        })
        return parsed_text,None
    except Exception as e:
        return "LLM Generation Error: Please Update the API_KEY",e
# --> Todo: Write the parser code using suitable framework
def pdf_parser():
    pass