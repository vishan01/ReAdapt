import subprocess
import tempfile
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Tuple

class LatexResumeOutput(BaseModel):
    latex_code: str
    reasoning: str

def compile_latex_to_pdf(latex_code:str)->tuple:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Compile LaTeX to PDF
        try:            
            os.system(f"pdflatex -interaction=nonstopmode --output-directory={tmpdir} {tex_path} ")
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            return pdf_bytes, None

        except subprocess.CalledProcessError as e:
            return "LaTeX compilation failed. Please check your LaTeX code.",e

def latex_code_generator(job_details: dict, template: str, extracted_resume: str) -> Tuple[str, str]:
    # Initialize the Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """
You are a professional resume formatter using LaTeX. Your task is to take the provided resume text and job description,
and rewrite the resume using the LaTeX template provided. Customize the content to best match the job description and skills.
Make sure to create a high-quality ATS friendly LaTeX resume. Include relevant keywords and sentences from the job description to enhance ATS compatibility.

Job Title: {job_title}
Required Skills: {skills}
Job Description: {job_description}

Original Resume Text:
{resume_text}

LaTeX Template:
{template}

Important things:
    1) Bold few points in projects description as per job
    2) Rewrite the hyperlinks in latex template as per given resume data
    3) Leave hyperlinks in the template if its not available in given resume
    
Output only the final LaTeX code for the resume and nothing else.

        """
    )

    # Chain
    chain = prompt | model | StrOutputParser()

    # Format prompt with variables
    job_details = job_details[0]  # Assuming job_details is a list with one dict
    input_data = {
        "job_title": job_details.get("job_title", ""),
        "skills": ", ".join(job_details.get("job_skills", [])),
        "job_description": job_details.get("job_description", ""),
        "resume_text": extracted_resume,
        "template": template
    }

    # Run the chain
    try:
        response = chain.invoke(input_data)

        latex_code=response.strip()

        return latex_code,""
    except Exception as e:
        return "Resume Generation Error",str(e)