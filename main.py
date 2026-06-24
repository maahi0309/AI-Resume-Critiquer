import streamlit as st
import PyPDF2
import io
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📄",
    layout="centered"
)

st.title("AI Resume Critiquer")
st.markdown(
    "Upload your resume in PDF format, and the AI will provide feedback and suggestions for improvement."
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Remove this line later after testing
st.write("API Key Loaded:", bool(GEMINI_API_KEY))

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"]
)

job_role = st.text_input(
    "Enter the job role you are applying for (optional):"
)

analyze = st.button("Analyze Resume")


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(
            io.BytesIO(uploaded_file.read())
        )

    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error(
                "The uploaded file is empty. Please upload a valid resume."
            )
            st.stop()

        prompt = f"""
        Please analyse this resume and provide constructive feedback.

        Focus on following aspects:
        1. content clarity and impact
        2. skills presentation
        3. experience description
        4. specific improvements for {job_role if job_role else "General Job Application"}

        Resume:
        {file_content}

        please provide your feedback in a clear, structured format with specific recommendations.
        """

        with st.spinner("Analyzing your resume..."):

            client = genai.Client(
                api_key=GEMINI_API_KEY
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

        st.success("Analysis Complete!")
        st.markdown("### AI Feedback and Suggestions")
        st.write(response.text)

    except Exception as e:
        st.error(
            f"An error occurred while processing the resume: {e}"
        )