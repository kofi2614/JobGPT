from flask import Flask, request, render_template
from jobgpt.resume_analyzer.resume_analyzer import ResumeAnalyzer
app = Flask(__name__)



@app.route('/', methods=['GET'])
def form():
    # Render the form template
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def process_strings():
    # Extract strings from the form data
    resume = request.form.get('resume')
    job_description = request.form.get('job_description')
    analyzer = ResumeAnalyzer()
    output = analyzer.analyze(resume, job_description)
    # You can now do whatever you need with the strings
    # For now, we'll just return them in a plain text response
    evaluation = output['evaluation']
    suggestion = output['suggestions']
    revised_resume = output['revised_resume']
    return render_template('result.html', evaluation=evaluation, suggestion=suggestion, original_resume=resume, revised_resume=revised_resume)


if __name__ == "__main__":
    app.run(debug=True)
