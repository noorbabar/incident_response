from flask import Flask, render_template, request, send_file
import json, os
from datetime import datetime
from utils import generate_timeline, generate_pdf_report

app = Flask(__name__)

with open('incidents.json') as f:
    INCIDENTS = json.load(f)

LOG_FILE = "log.txt"

@app.route('/')
def index():
    return render_template('index.html', incidents=INCIDENTS)

@app.route('/simulate', methods=['POST'])
def simulate():
    incident_type = request.form.get('incident_type')
    severity = request.form.get('severity')
    custom_desc = request.form.get('description', '').strip()

    response_data = INCIDENTS.get(incident_type, {}).get(severity, {})
    timeline = generate_timeline(response_data)

    log_entry = {
        "incident": incident_type,
        "severity": severity,
        "description": custom_desc,
        "timestamp": datetime.now().isoformat()
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

    return render_template('index.html', incidents=INCIDENTS,
                           response=response_data, selected=incident_type,
                           severity=severity, timeline=timeline,
                           description=custom_desc)

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE):
        return "No logs yet."
    
    with open(LOG_FILE) as f:
        entries = [json.loads(line) for line in f]
    
    return render_template('logs.html', logs=entries)

@app.route('/download-report')
def download_report():
    path = generate_pdf_report()
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
