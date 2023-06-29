"""Read resume in pdf format and return a string of text"""

import fitz

class ResumeReader:
    def __init__(self):
        pass
    def read(self, pdf_path):
        texts = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                texts.append(page.get_text())
        return texts

if __name__ == '__main__':
    
    # Provide the path to your resume PDF file
    resume_path = 'data/resume_pdf/resume_1.pdf'

    # Extract text from the resume PDF
    resume_text = ResumeReader().read(resume_path)

    # Print the extracted text
    print(resume_text)