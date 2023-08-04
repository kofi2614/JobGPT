from flask import Flask, request, jsonify, render_template
from jobgpt.resume_processor.resume_analyzer import ResumeAnalyzer
from jobgpt.resume_processor.resume_reader import ResumeReader
from jobgpt.resume_processor.resume_segmenter import ResumeSegmenter
from jobgpt.resume_processor.base import ResumeProcessor
from jobgpt.utils.text_processor import process_text_for_html
import io
import asyncio
import json

app = Flask(__name__)

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
    jd = json.dumps(process_text_for_html(request.form['job_description']))
    byte_stream = io.BytesIO(file.stream.read())        
    processed_resume = asyncio.run(ResumeProcessor().process(byte_stream, jd))    
    with open('local/processed_resume.json', 'w') as f:
        json.dump(processed_resume, f, indent=4)
    for segment in processed_resume:
        if segment:
            segment['analysis'] = process_text_for_html(segment['analysis'])
            segment['content'] = process_text_for_html(segment['content'])           
    processed_resume_str = json.dumps(processed_resume)   
    print(processed_resume_str)
    return render_template('segmented_resume.html', segmented_resume=processed_resume_str, jd=jd)                          

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
    app.run(host="0.0.0.0", port=8080)