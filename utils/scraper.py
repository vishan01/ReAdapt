from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate


class JobInfo(BaseModel):
    job_title: str
    job_skills: str
    job_description: str

parser = JsonOutputParser(pydantic_object=JobInfo)

prompt = PromptTemplate.from_template("""
Extract the job information from the text below and respond in the specified JSON format.

{format_instructions}

Job Posting:
{job_posting}
""")
