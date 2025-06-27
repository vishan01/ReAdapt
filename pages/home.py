import streamlit as st
st.set_page_config("Home")
st.title("_ReAdapt_: Adapt :blue[Resume] as per :orange[Job]")
uploaded_file=st.file_uploader("Upload Your Resume")
if 'job_info' not in st.session_state:
    st.session_state['job_info']=None
if uploaded_file:
    st.selectbox("Select Job Description/Link",["URL","TEXT"],placeholder="Choose your option")