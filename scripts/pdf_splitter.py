import PyPDF2

def split_pdf(pdf_path):
    pdfs = []
    cnt = 1
    pdf = PyPDF2.PdfReader(pdf_path)
    for page in range(len(pdf.pages)):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf.pages[page])
        output = f'data/resumes/resume_{cnt}.pdf'
        if page in [0,3,6,9,14]:
            with open(output, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            pdfs.append(output)
            cnt += 1
    return pdfs

# Provide the path to your PDF file
pdf_path = 'data/resumes/resumes.pdf'

# Split the PDF into separate pages
pdfs = split_pdf(pdf_path)
print(pdfs)