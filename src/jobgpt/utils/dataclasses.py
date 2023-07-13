from abc import abstractmethod
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Section(BaseModel):

    @abstractmethod
    def to_list(self):
        pass
    
    def to_str(self):
        return "\n".join(self.to_list())
    
    def to_str_html(self):
        return "\\n".join(self.to_list())        

class WorkExperience(BaseModel):
    title: str = Field(description="The title of the position")
    company: str = Field(description="The company of the position")
    bullet_points: List[str] = Field(description="The list of text that describes the experience")
    def to_list(self):
        output = [self.title, self.company]
        bullet_list = ["* "+bullet for bullet in self.bullet_points]
        output.extend(bullet_list)
        return output

class WorkExperienceSection(Section):
    work_experiences: List[WorkExperience] = Field(description="The list of work experiences")

    def to_list(self):
        we_list = []
        for we in self.work_experiences:
            we_list.extend(we.to_list())
            we_list.append("")
        return we_list

class Education(BaseModel):
    school: str = Field(description="The school of the education")
    degree: str = Field(description="The degree of the education")
    major: str = Field(description="The major of the education")
    bullet_points: Optional[List[str]] = Field(description="The list of text that describes the education")

    def to_list(self):
        output = [self.school, self.degree, self.major]
        bullet_list = ["* "+bullet for bullet in self.bullet_points]
        output.extend(bullet_list)
        return output

class EducationSection(Section):
    educations: List[Education] = Field(description="The list of educations") 

    def to_list(self):
        edu = []
        for e in self.educations:
            edu.extend(e.to_list())
            edu.append("")
        return edu   

class PersonalProject(BaseModel):
    title: str = Field(description="The title of the project")
    bullet_points: List[str] = Field(description="The list of text that describes the project and the canditate's contribution")

    def to_list(self):
        output = [self.title]
        bullet_list = ["* "+bullet for bullet in self.bullet_points]
        output.extend(bullet_list)
        return output

class PersonalProjectSection(Section):
    personal_projects: List[PersonalProject] = Field(description="The list of personal projects")

    def to_list(self):
        pp_list = []
        for pp in self.personal_projects:
            pp_list.extend(pp.to_list())
            pp_list.append("")
        return pp_list
      
class SummarySection(Section):
    bullet_points: List[str] = Field(description="The summary or highlight of the resume which usually appears at the top or buttom of the resume")

    def to_list(self):
        return ["* " + t for t in self.bullet_points]    

class SkillsSection(Section):
    bullet_points: List[str] = Field(description="The list of skills that the candidate has")

    def to_list(self):
        return ["* " + t for t in self.bullet_points]





class SegmentedResume(BaseModel):
    work_experiences: WorkExperienceSection = Field(description="The work experience section of the resume")
    educations: EducationSection = Field(description="The education section of the resume")
    personal_projects: Optional[PersonalProjectSection] = Field(description="The project section of the resume. It can be personal project, research project, case study or attended competition")
    summary: Optional[SummarySection] = Field(description="The summary section of the resume")
    skills: Optional[SkillsSection] = Field(description="The skills section of the resume")

    def to_list(self):                
        return [
            {"title": "Summary", "content": self.summary.to_str_html()} if self.summary else None,
            {"title": "Work Experience", "content": self.work_experiences.to_str_html()} if self.work_experiences else None,
            {"title": "Education", "content": self.educations.to_str_html()} if self.educations else None,
            {"title": "Personal Projects", "content": self.personal_projects.to_str_html()} if self.personal_projects else None,            
            {"title": "Skills", "content": self.skills.to_str_html()} if self.skills else None                          
        ]
    

class AnalyzedSection(BaseModel):
    evaluation: str = Field(description="The detailed evaluation of the section")
    suggestion: List[str] = Field(description="The list of suggestions that you think the user should improve in this section")
    revised_section: Section = Field(description="The revised section of the resume that you think the user should use")