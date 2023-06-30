from pydantic import BaseModel, Field, validator
from typing import List, Optional

class WorkExperience(BaseModel):
    title: str = Field(description="The title of the position")
    company: str = Field(description="The company of the position")
    bullet_points: List[str] = Field(description="The list of text that describes the experience")

class Education(BaseModel):
    school: str = Field(description="The school of the education")
    degree: str = Field(description="The degree of the education")
    major: str = Field(description="The major of the education")
    bullet_points: List[str] = Field(description="The list of text that describes the education")

class PersonalProject(BaseModel):
    title: str = Field(description="The title of the project")
    bullet_points: List[str] = Field(description="The list of text that describes the project and the canditate's contribution")

class Summary(BaseModel):
    text: List[str] = Field(description="The summary or highlight of the resume which usually appears at the top or buttom of the resume")

class Skills(BaseModel):
    text: List[str] = Field(description="The list of skills that the candidate has")

class SegmentedResume(BaseModel):
    work_experiences: List[WorkExperience] = Field(description="The work experience section of the resume")
    educations: List[Education] = Field(description="The education section of the resume")
    personal_projects: Optional[List[PersonalProject]] = Field(description="The project section of the resume. It can be personal project, research project, case study or attended competition")
    summary: Optional[Summary] = Field(description="The summary section of the resume")
    skills: Optional[Skills] = Field(description="The skills section of the resume")