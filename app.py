import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Load all environment variables

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from Gemini model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from the uploaded PDF resume
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt template for Gemini model
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide 
the best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response as per below structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit UI
with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("""
    This sophisticated ATS project, developed with Gemini Pro and Streamlit, seamlessly incorporates advanced features 
    including resume match percentage, keyword analysis to identify missing criteria, and the generation of comprehensive 
    profile summaries, enhancing the efficiency and precision of the candidate evaluation process for discerning talent acquisition professionals.
    """)
    add_vertical_space(5)
    st.write("Made with ❤ by Hariom.")

st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        # Prepare input prompt for the model
        prompt = input_prompt.format(text=resume_text, jd=jd)
        # Get the response from Gemini model
        response = get_gemini_response(prompt)
        st.subheader(response)
