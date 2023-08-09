import json
import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from jobgpt.resume_processor.resume_reader import ResumeReader
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from jobgpt.utils.llm import count_tokens, load_model
from typing import Dict
from jobgpt.utils.dataclasses import SummarySection, SkillsSection, WorkExperienceSection, EducationSection, PersonalProjectSection


system_template = """
You are an experienced career consultalt who helps clients to improve their resumes.
When you are asked to provide evaluation or suggestion, make sure your are critical and specific.
Focus on the use of professional language and the relevancy to the job description.
""".strip()

skills_template = """
You are a experienced career consultalt helping clients with the skills section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.

First, give an CRITICAL evaluation of the skills section focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the skills section besed on your suggestions.

Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
REMEMBER DO NOT make things up or create fake experiences. 

Your output should always be in JSON format with following fields:
- Evaluation: a list of strings, each string is an evaluation of a work experience
- Suggestions: a list of strings, each string is a suggestion of a work experience,
- Revision: a list of strings, each string is a revision of a work experience bullet point.

Make sure to add proper line breaker "\n" in your response so that format is pretty.


{section}: {section_text}
Job Description: {job_description}
""".strip()

work_experience_template = """
You are a experienced career consultalt helping clients with the work experience section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
First, give an CRITICAL evaluation of the work experience section focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the work experience section besed on your suggestions

Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
REMEMBER DO NOT make things up or create fake experiences. 

Your output should always be in JSON format with following fields:
- Evaluation: a list of strings, each string is an evaluation of a work experience
- Suggestions: a list of strings, each string is a suggestion of a work experience,
- Revision: a list of strings, each string is a revision of a work experience bullet point.

Make sure to add proper line breaker "\n" in your response so that format is pretty.

{section}: {section_text}
Job Description: {job_description}
""".strip()

education_template = """
You are a experienced career consultalt helping clients with the education section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
First, give an CRITICAL evaluation of the education section focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the education section besed on your suggestions.

Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
REMEMBER DO NOT make things up or create fake experiences. 

Your output should always be in JSON format with following fields:
- Evaluation: a list of strings, each string is an evaluation of a work experience
- Suggestions: a list of strings, each string is a suggestion of a work experience,
- Revision: a list of strings, each string is a revision of a work experience bullet point.

Make sure to add proper line breaker "\n" in your response so that format is pretty.

{section}: {section_text}
Job Description: {job_description}
""".strip()

summary_template = """
You are a experienced career consultalt helping clients with the summary section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
First, give an CRITICAL evaluation of the summary section focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the summary section besed on your suggestions.

Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
REMEMBER DO NOT make things up or create fake experiences. 

Your output should always be in JSON format with following fields:
- Evaluation: a list of strings, each string is an evaluation of a work experience
- Suggestions: a list of strings, each string is a suggestion of a work experience,
- Revision: a list of strings, each string is a revision of a work experience bullet point.

Make sure to add proper line breaker "\n" in your response so that format is pretty.

{section}: {section_text}
Job Description: {job_description}
""".strip()

personal_project_template = """
You are a experienced career consultalt helping clients with the personal project section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
First, give an CRITICAL evaluation of the personal project section focusing on use of professional language and the relevancy to the job description.
Second, provide suggestions on how the client can improve the section. Mention the exact wording used and how the client can reword it. 
Try to find all the problems and give specific suggestions.
Last, give a revision of the personal project section besed on your suggestions.

Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
REMEMBER DO NOT make things up or create fake experiences. 

Your output should always be in JSON format with following fields:
- Evaluation: a list of strings, each string is an evaluation of a work experience
- Suggestions: a list of strings, each string is a suggestion of a work experience,
- Revision: a list of strings, each string is a revision of a work experience bullet point.

Make sure to add proper line breaker "\n" in your response so that format is pretty.

{section}: {section_text}
Job Description: {job_description}
""".strip()

section_title_map = {
    "Skills": "skills",
    "Work Experience": "work_experience",
    "Education": "education",
    "Summary": "summary",
    "Personal Projects": "personal_project"    
}
prompt_map = {
    "skill": skills_template,
    "work_experience": work_experience_template,
    "education": education_template,
    "summary": summary_template,
    "personal_project": personal_project_template
}

section_model_map = {
    "skill": SkillsSection,
    "work_experience": WorkExperienceSection,
    "education": EducationSection,
    "summary": SummarySection,
    "personal_project": PersonalProjectSection    
}

class ResumeSectionAnalyzer:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.0):
        self.llm = load_model(model_name, temperature=temperature)        
        self.system_prompt = SystemMessagePromptTemplate.from_template(system_template.strip())        
    async def analyze(self, section_title: str, section_text: str, job_description: str) -> dict:                
        user_prompt = HumanMessagePromptTemplate.from_template(prompt_map[section_title])
        resume_analyzer_prompt = ChatPromptTemplate(input_variables=["section", "section_text", "job_description"], messages=[self.system_prompt, user_prompt])
        chain_analyze = LLMChain(llm=self.llm, prompt=resume_analyzer_prompt)
        analysis = await chain_analyze.arun(
            {                   
                "section": section_title, 
                "section_text": section_text, 
                "job_description": job_description
            })  
        output = {"title": section_title, "analysis": analysis}              
        return output