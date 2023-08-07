from jobgpt.resume_processor.resume_section_analyzer import ResumeSectionAnalyzer
from jobgpt.resume_processor.resume_segmenter import ResumeSegmenter
from jobgpt.resume_processor.resume_reader import ResumeReader
from typing import Union
import asyncio
import json
import io

class ResumeProcessor:
    def __init__(self, segmenter_model = "gpt-3.5-turbo", segmenter_temperature: float = 0.0, analyzer_model = "gpt-3.5-turbo", analyzer_temperature: float = 0.0):
        self.reader = ResumeReader()
        self.segmenter = ResumeSegmenter(segmenter_model, segmenter_temperature)
        self.analyzer = ResumeSectionAnalyzer(analyzer_model, analyzer_temperature)
    async def process(self, resume_path: Union[str, io.BytesIO], jd: str):
        resume = self.reader.read(resume_path)        
        segmented_resume = self.segmenter.segment(resume)
        analyzer_inputs = [
            (k, v, jd) for k, v in segmented_resume.items() if v
        ]
        tasks = [self.analyzer.analyze(*analyzer_input) for analyzer_input in analyzer_inputs]        
        analyzed_resume = await asyncio.gather(*tasks)
        for section in analyzed_resume:
            section['content'] = segmented_resume[section['title']]
        return analyzed_resume
