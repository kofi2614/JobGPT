from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from jobgpt.utils.llm import load_model


system_template = """
You are an experienced career consultalt who helps clients to improve their resumes.
When you are asked to provide evaluation or suggestion, make sure your are critical and specific.

REMEMBER DO NOT make things up or create fake experiences. 
""".strip()

resume_full_template = """
You are a experienced career consultalt helping clients with the skills section of their resumes given a job description that the client is applying for.
Let's think step by step and experience by experience.
Your consideration should include but not limited to the following aspects:
(1) Whether the wording in the resume is professional and appropriate.
(2) Whether measurable results are used to describe the experience.
(3) Whether the experience is relevant to the job description.
(4) Whether the key words in the job description are used in the resume. 
    Note that client may not have all the skills or experiences required in the job description.
(5) Make sure that no common cliches and buzzwords are used in the resume.
(6) Any other issues or rooms for improvement you can find in the resume.
First, give an overall evaluation of the resume
Second, provide suggestions on how the client can improve the resume. Mention the exact wording used and how the client can refine it.
Try to find all the problems and give specific suggestions.

resume: {resume_text}
Job Description: {job_description}
""".strip()


class ResumeFullAnalyzer:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = load_model(model_name)        
        self.system_prompt = SystemMessagePromptTemplate.from_template(system_template.strip())        
    async def analyze(self,resume_text: str, job_description: str) -> dict:                
        user_prompt = HumanMessagePromptTemplate.from_template(resume_full_template)
        resume_analyzer_prompt = ChatPromptTemplate(input_variables=["resume_text", "job_description"], messages=[self.system_prompt, user_prompt])
        chain_analyze = LLMChain(llm=self.llm, prompt=resume_analyzer_prompt)
        analysis = await chain_analyze.arun(
            {                                   
                "resume_text": resume_text, 
                "job_description": job_description
            })                
        return analysis