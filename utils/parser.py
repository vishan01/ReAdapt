from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import pymupdf4llm
import pymupdf
import tempfile

class JobInfo(BaseModel):
    job_title: str
    job_skills: str
    job_description: str

def parse_job_posting(job_posting_text: list[str]) -> JobInfo|tuple:
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
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    chain = prompt | llm | parser
    try:
        parsed_text=chain.invoke({
            "job_posting": "\n".join(job_posting_text),
            "format_instructions": format_instructions
        })
        return parsed_text,None
    except Exception as e:
        return "LLM Generation Error: Please Update the API_KEY",e
    
def pdf_parser(file)->str:
    pdf_path=""
    md_text=""
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "resume.pdf")
        with open(pdf_path,'wb') as res_writer:
            res_writer.write(file.getvalue())
        md_text = pymupdf4llm.to_markdown(pymupdf.Document(pdf_path))
    return md_text