from flask import Flask, request, render_template

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

    # You can now do whatever you need with the strings
    # For now, we'll just return them in a plain text response
    return f'resume: {resume}\n resume: {job_description}'

if __name__ == "__main__":
    app.run(debug=True)
