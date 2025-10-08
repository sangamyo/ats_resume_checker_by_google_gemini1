import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv() # Load all the environment variables from .env

# ----------------------------
# Configure Gemini API Key from Streamlit Secrets
# ----------------------------
# Make sure you have set the API key in Streamlit Secrets as:
# GOOGLE_API_KEY="your_api_key_here"
api_key = os.getenv("GOOGLE_API_KEY")  # <- Use Streamlit Secrets

genai.configure(api_key=api_key)

# ----------------------------
# Initialize Gemini Model (cached)
# ----------------------------
@st.cache_resource
def get_gemini_model():
    return genai.GenerativeModel('models/gemini-pro-latest')

# ----------------------------
# Function to get a response from Gemini model (cached)
# ----------------------------
@st.cache_data
def get_gemini_response(prompt):
    model = get_gemini_model()
    try:
        response = model.generate_content(prompt, timeout=180)  # 3 minutes
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# Function to extract text from PDF
# ----------------------------
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += str(page_text)
    return text

# ----------------------------
# Function to chunk large text
# ----------------------------
def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ----------------------------
# Prompt template
# ----------------------------
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide 
the best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.

Resume:
{text}

Job Description:
{jd}

I want the response as per below structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# ----------------------------
# Streamlit UI
# ----------------------------
with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("""
    This sophisticated ATS project, developed with Gemini Pro and Streamlit, seamlessly incorporates advanced features 
    including resume match percentage, keyword analysis to identify missing criteria, and the generation of comprehensive 
    profile summaries, enhancing the efficiency and precision of the candidate evaluation process.
    """)
    add_vertical_space(5)
    st.write("Made with ❤ by Hariom.")

st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF file")
submit = st.button("Submit")

# ----------------------------
# Processing
# ----------------------------
if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        chunks = chunk_text(resume_text, chunk_size=1000)
        full_response = ""
        for i, chunk in enumerate(chunks):
            prompt = input_prompt.format(text=chunk, jd=jd)
            with st.spinner(f"Analyzing chunk {i+1}/{len(chunks)}..."):
                response = get_gemini_response(prompt)
            full_response += response + "\n"
        st.subheader("ATS Analysis Result")
        st.text(full_response)
    else:
        st.error("Please upload a PDF resume to proceed.")
