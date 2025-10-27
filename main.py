import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from utils.parser import pdf_parser,parse_job_posting
from utils.scraper import retrieve_data
from utils.generator import latex_code_generator,compile_latex_to_pdf
import config
import base64
st.set_page_config("Home")
st.title("_ReAdapt_: Adapt :blue[Resume] as per :orange[Job]")
uploaded_file=st.file_uploader("Upload Your Resume")
if 'resume' not in st.session_state:
    st.session_state['resume']=None

if uploaded_file:
    with st.spinner("Parsing Resume"):
        st.session_state['resume']=pdf_parser(uploaded_file)

if 'job_info' not in st.session_state:
    st.session_state['job_info']={}

job_desc=st.text_area("Enter the Job Description")

if st.button("Generate Resume"):
    if job_desc and st.session_state['resume']:
        with st.spinner("Parsing Job Description"):
            st.session_state['job_info']['job_desc']=parse_job_posting([job_desc])
        if st.session_state['job_info'].get('job_desc',None):
            with open("template.tex","r") as file:
                template=file.read()
                with st.spinner("Generating LaTeX Code"):
                    latex_code,reason=latex_code_generator(st.session_state['job_info']['job_desc'],template,st.session_state['resume'])
                    if st.toggle("View Generated Latex Code:"):
                        st.write(latex_code)
                with st.spinner("Compiling LaTeX to PDF"):
                    pdf,err=compile_latex_to_pdf(latex_code)
                if not err:
                    pdf_viewer(pdf, width=700, height=1000)
    else:
        st.warning("Please upload your resume and enter the job description.")