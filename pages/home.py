import streamlit as st
from ..utils.parser import pdf_parser,parse_job_posting
from ..utils.scraper import retrieve_data

st.set_page_config("Home")
st.title("_ReAdapt_: Adapt :blue[Resume] as per :orange[Job]")
uploaded_file=st.file_uploader("Upload Your Resume")
if 'resume' not in st.session_state:
    st.session_state['resume']=None

with st.spinner("Parsing Resume"):
    st.session_state['resume']=pdf_parser(uploaded_file)

if 'job_info' not in st.session_state:
    st.session_state['job_info']={}

if st.session_state['resume']:
    st.session_state['job_info']['type']=st.selectbox("Select Job Description/Link",["URL","TEXT"],placeholder="Choose your option")

if st.session_state['job_info'].get('type',None)=="URL":
    job_url=st.text_input("Enter the URL of the job")
    if job_url:
        with st.status("Parsing job description from url"):
            try:
                st.write("Scraping the website")
                data=retrieve_data(job_url)
                st.write("Parsing data")
                parsed_data=parse_job_posting(data)
                st.session_state['job_info']['job_desc']=parsed_data
            except Exception as e:
                st.error("There has been an error parsing Job Description")
elif st.session_state['job_info'].get('type',None)=="TEXT":
    job_desc=st.text_area("Enter the Job Description")
    with st.spinner("Parsing Job Description"):
        st.session_state['job_info']['job_desc']=parse_job_posting([job_desc])
