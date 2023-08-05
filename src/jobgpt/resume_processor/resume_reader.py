"""Read resume in pdf format and return a string of text"""

import fitz
import io
from typing import Union
from jobgpt.utils.text_processor import process_text

class ResumeReader:
    def __init__(self):
        pass
    def read(self, pdf: Union[str, io.BytesIO]):        
            
        texts = []
        if isinstance(pdf, str):
            doc = fitz.open(pdf)
        elif isinstance(pdf, io.BytesIO):
            doc = fitz.open(stream=pdf, filetype="pdf")        
        for page in doc:
            texts.append(page.get_text())
        text = "\n".join(texts)
        text = process_text(text)
        return text 
  