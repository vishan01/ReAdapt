import streamlit as st
st.set_page_config("Home")
st.title("_ReAdapt_: Adapt :blue[Resume] as per :orange[Job]")
uploaded_file=st.file_uploader("Upload Your Resume")

if 'job_info' not in st.session_state:
    st.session_state['job_info']={}

if uploaded_file:
    st.session_state['job_info']['type']=st.selectbox("Select Job Description/Link",["URL","TEXT"],placeholder="Choose your option")

if st.session_state['job_info']=="URL":
    job_url=st.text_input("Enter the URL of the job")
else:
    job_desc=st.text_area("Enter the Job Description")
    st.session_state['job_info']['job_desc']=job_desc