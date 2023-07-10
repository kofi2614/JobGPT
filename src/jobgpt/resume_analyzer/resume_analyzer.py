import json
import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from jobgpt.resume_analyzer.resume_reader import ResumeReader
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from jobgpt.utils.llm import count_tokens, load_model
from typing import List

system_template = """
You are an experienced career consultalt who helps clients to improve their resumes.
When you are asked to provide evaluation or suggestion, make sure your are critical and specific.
Focus on the use of professional language and the relevancy to the job description.
REMEMBER DO NOT make things up or create fake experiences. 

You response should be in JSON format with following keys: "evaluation", "suggestions", "revised_resume".
"""
user_teamplate = """
You are a experienced career consultalt helping clients with the {section} section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
First, give an CRITICAL evaluation of the {section} focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the {section} section besed on your suggestions.

{section}: {section_text}
Job Description: {job_description}
"""

class ResumeAnalyzer:
    def __init__(self):
        self.llm = load_model()
        system_prompt = SystemMessagePromptTemplate.from_template(system_template.strip())
        user_prompt = HumanMessagePromptTemplate.from_template(user_teamplate.strip())
        resume_analyzer_prompt = ChatPromptTemplate(input_variables=["section", "section_text", "job_description"], messages=[system_prompt, user_prompt])
        self.chain_analyze = LLMChain(llm=self.llm, prompt=resume_analyzer_prompt)
    def analyze(self, section_text: str, job_description: str, section: str = 'work experience') -> dict:
        
        output = count_tokens(self.chain_analyze, 
                              {"section": section, 
                               "section_text": section_text, 
                               "job_description": job_description
                               })
        output_dict = json.loads(output['result'])
        return output_dict