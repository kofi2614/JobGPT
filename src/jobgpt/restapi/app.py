from flask import Flask, request, jsonify, render_template
from jobgpt.resume_analyzer.resume_analyzer import ResumeAnalyzer
from jobgpt.resume_analyzer.resume_reader import ResumeReader
from jobgpt.resume_analyzer.resume_segmenter import ResumeSegmenter
import io
import asyncio
import json

app = Flask(__name__)

with open('local/analyzed_resume.json', 'r') as f:
    segmented_resume = json.load(f)  

@app.route('/', methods=['GET'])
def form():
    # Render the form template
    return render_template('index.html')

@app.route('/segment', methods=['POST'])
def process_resumes():
    # Extract strings from the form data
    if 'resume' not in request.files:
        return 'No Resume Found'
    file = request.files['resume']
    if not file or file.filename == '':        
        return 'No Resume Found'
    jd = request.form['job_description']
    byte_stream = io.BytesIO(file.stream.read())
    resume = ResumeReader().read(byte_stream)
    analyzer = ResumeAnalyzer()
    segmented_resume = ResumeSegmenter("gpt-4").segment(resume).to_list()    
    # for resume_segment in segmented_resume:
    #     if resume_segment:
    #         resume_segment['analysis'] = analyzer.analyze(resume_segment, jd)                    
    # print(segmented_resume)    
    for segment in segmented_resume:
        if segment:
            segment['analysis'] = segment['analysis'].replace('\n', '\\n')
            segment['analysis'] = segment['analysis'].replace("""\"""", '')
    return render_template('segmented_resume.html', segmented_resume=segmented_resume, jd=jd)                          

@app.route('/followup', methods=['POST'])
def followup():
    data = request.get_json()  # get the incoming data
    
    title = data.get('title')    
    content = data.get('content')
    original_analysis = data.get('analysis')
    jd = data.get('jd')
    print(content)
    print(title)
    analyzer = ResumeAnalyzer()
    analysis_input = {'title': title, 'content': content}
    new_analysis = analyzer.analyze(analysis_input, jd)   
   

    # Return the new values as JSON
    return jsonify({"analysis": new_analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)