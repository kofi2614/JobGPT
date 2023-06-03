"""Read resume in pdf format and return a string of text"""

import fitz

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Provide the path to your resume PDF file
resume_path = 'data/resumes/resume_1.pdf'

# Extract text from the resume PDF
resume_text = extract_text_from_pdf(resume_path)

# Print the extracted text
print(resume_text)