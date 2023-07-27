"""Read resume in pdf format and return a string of text"""

import fitz
import io
from typing import Union

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
        return texts 
  