import os
import sys
import json
from jobgpt.resume_analyzer.resume_reader import ResumeReader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
user_template = """
You will be given a page of text and the text of its previous page. 
The text can only be one of two types: A candidate's resume or job description.
If you think this page is a resume, return the name of the candidate connecting first anmd last name with underscore.
For example, John Doe should be written as john_doe.
If you cannot tell the name from a resume, then it must be a job description.
If the page is not resume, then it MUST be job description.Return the name of the job position connected with underscore.
For example, Data Scientist should be written as data_scientist. 
If you can't find the job position, just say "unknown".
Return your output in JSON format with the following keys: page_type, name.

text: {text}
"""
def write_file(content, filename):
    # Split the filename into the name and the extension
    base, extension = os.path.splitext(filename)
    
    counter = 1
    while os.path.exists(filename):
        # If the file exists, increment the counter and append it to the filename
        counter += 1
        filename = f"{base}-{counter}{extension}"
    
    # Once we've found a filename that doesn't exist, write to it
    with open(filename, 'w') as f:
        f.write(content)

human_message_prompt = HumanMessagePromptTemplate.from_template(user_template)
chat = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.7,
    verbose=True,
)
chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
file = sys.argv[1]
# file = 'Room02_Weizheng_Rita_Miki.pdf'
filename = f'data/resume_books/{file}'
resume_reader = ResumeReader()
resume_texts = resume_reader.read(filename)
job_description = {}
for i, text in enumerate(resume_texts):
    if text:
        print(f"page: {i}")
        response = chat(chat_prompt.format_prompt(text=text).to_messages()).content
        print(response)
        response = json.loads(response)
        if response['page_type'] == 'resume' and response['name']!='unknown':
            filename = f'data/resume_txt/{response["name"]}.txt'
            write_file(text, filename)
            if job_description and job_description["text"]!='unknown':
                filename = f'data/job_descriptions/{job_description["name"]}.txt'
                write_file(job_description["text"], filename)
                job_description = {}
        else:
            if job_description:
                job_description["text"] += text
            else:
                job_description["text"] = text
                job_description["name"] = response["name"]
 