from flask import Flask, request, jsonify, render_template
from jobgpt.resume_analyzer.resume_analyzer import ResumeAnalyzer
from jobgpt.resume_analyzer.resume_reader import ResumeReader
from jobgpt.resume_analyzer.resume_segmenter import ResumeSegmenter
import io
import asyncio
import json

app = Flask(__name__)

TEXT = ['Client Ops Analyst/nJP Morgan Chase Bank, Shanghai, China/nCommunicated with clients and internal teams (KYC Officers, Relationship Management and Compliance) from China and overseas to update clients’ credit profile and monitor key credit risk events/nPerformed periodic risk analysis for corporate clients across various sectors to identify potential credit issues and adjust clients’ credit rating following internal procedure and Compliance’s requirements/nDeveloped risk assessment reports for clients on Macroeconomic and Microeconomic factors (Countries, Organization structure, financials and etc.) and evaluated credit risk events with relationship management team/nBuilt report to track potential screening alerts which affected client’s credit risk rating and led the team to collect over 10,000 alerts for more than 500 companies in 3 months and escalated to Compliance team/nTrained 3 new analysts with process to analyze clients’ profile and assess risk ratings and framework to complete risk assessment reports following internal policy', 'Business Performance Management Analyst/nMUFG, Toronto, Canada/nCooperated with members of Relationship Management, Portfolio Management, Compliance and other stakeholders to consistently monitor clients’ credit risk and update clients’ portfolio/nPerformed periodic Due Diligence with clients’ reports for companies across several sectors following Compliance’s policies and business requirements and updated clients’ risk rating/nConducted business and financial analysis with Portfolio Management teams and set up credit/trading limits for credit facilities and market lines (FX and SWAP Lines) based on credit agreements/nMonitored key credit issues for clients, communicated with relationship management team regarding to clients’ credit risk factors and prepared timely and accurate risk analysis reports to assist in internal credit rating adjustment/nProvided support to the upgrade of internal operation manual with Relationship Management team, Treasury and Compliance to comply with updated policy requirements from FINTRAC and OSFI', 'Business Support Analyst/nCIBC, Toronto, Canada/nActed as key liaison between various stakeholders, including senior management team, technical team and operation team to improve accuracy and efficiency of KYC analysis/nEvaluated transaction activities and account information for target clients and prepared transaction report to identify suspicious transaction pattern and risk factors related/nConducted periodic Due Diligence, analyzed clients’ financial and operating information to identify key credit risk factors and corresponding mitigation and updated clients’ risk rating accordingly/nPrepared detailed introduction of risk assessment for clients from various sectors and led the peer-to-peer training program to improve the efficiency of onboarding process for new colleagues/nOrganized the automation projects with technical team to generate and sort clients’ transaction information automatically and improved the efficiency of transaction analysis by 20%']

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
    # analyzer = ResumeAnalyzer()
    # segmented_resume = ResumeSegmenter("gpt-4").segment(resume).to_list()    
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