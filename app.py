from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

with open('incidents.json') as f:
    INCIDENTS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', incidents=INCIDENTS)

@app.route('/simulate', methods=['POST'])
def simulate():
    incident_type = request.form.get('incident_type')
    response = INCIDENTS.get(incident_type, {})
    
    log_entry = {
        "incident": incident_type,
        "timestamp": datetime.now().isoformat()
    }
    with open('log.txt', 'a') as log:
        log.write(json.dumps(log_entry) + "\n")
    
    return render_template('index.html', incidents=INCIDENTS, response=response, selected=incident_type)

if __name__ == '__main__':
    app.run(debug=True)
