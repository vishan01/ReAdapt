import streamlit as st
from utils.parser import pdf_parser,parse_job_posting
from utils.scraper import retrieve_data
from utils.generator import latex_code_generator,compile_latex_to_pdf

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

if st.session_state['resume']:
    st.session_state['job_info']['type']=st.selectbox("Select Job Description/Link",["URL","TEXT"],placeholder="Choose your option")

if st.session_state['job_info'].get('type',None)=="URL":
    job_url=st.text_input("Enter the URL of the job")
    if job_url:
        parsed_data,er=None,None
        with st.status("Parsing job description from url"):
            try:
                st.write("Scraping the website")
                data=retrieve_data(job_url)
                st.write("Parsing data")
                parsed_data,er=parse_job_posting(data)
                st.session_state['job_info']['job_desc']=parsed_data
            except Exception as e:
                st.error("There has been an error parsing Job Description, Please check the url")
        if er:
            st.write("Extremely sorry; Couldn't extract the description please provide it manually")
elif st.session_state['job_info'].get('type',None)=="TEXT":
    job_desc=st.text_area("Enter the Job Description")
    with st.spinner("Parsing Job Description"):
        st.session_state['job_info']['job_desc']=parse_job_posting([job_desc])

if st.session_state['job_info'].get('job_desc',None):
    with open("template.tex","r") as file:
        template=file.read()
        latex_code,reason=latex_code_generator(st.session_state['job_info']['job_desc'],template,st.session_state['resume'])
        pdf,err=compile_latex_to_pdf(latex_code)
        if not err:
            st.download_button("Download Resume",pdf,file_name="Resume.pdf",mime='application/octet-stream')