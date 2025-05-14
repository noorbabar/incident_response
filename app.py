from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import json
import os
from datetime import datetime
from utils import generate_timeline, generate_pdf_report

app = Flask(__name__)
app.secret_key = os.urandom(24)  

try:
    with open('incidents.json') as f:
        INCIDENTS = json.load(f)
except FileNotFoundError:
    # file != exist, then below should come up 
    INCIDENTS = {
        "Ransomware Attack": {
            "Low": {
                "Containment": "Isolate affected systems",
                "Recovery": "Restore from backups",
                "NIST": "PR.IP-4: Backups of information are conducted, maintained, and tested",
                "ASD 8": "Regular backups"
            },
            "Medium": {
                "Containment": "Network segmentation",
                "Recovery": "Rebuild systems from trusted images",
                "NIST": "DE.CM-1: The network is monitored to detect potential cybersecurity events",
                "ASD 8": "Multi-factor authentication"
            },
            "High": {
                "Containment": "Complete network isolation",
                "Recovery": "Full system recovery and investigation",
                "NIST": "RS.MI-1: Incidents are contained",
                "ASD 8": "Patch applications and operating systems"
            }
        },
        "Phishing Campaign": {
            "Low": {
                "Containment": "Block sender domains",
                "Recovery": "User awareness training",
                "NIST": "PR.AT-1: All users are informed and trained",
                "ASD 8": "User application hardening"
            },
            "Medium": {
                "Containment": "Password resets for targeted users",
                "Recovery": "Scan for indicators of compromise",
                "NIST": "DE.DP-4: Event detection information is communicated",
                "ASD 8": "Restrict administrative privileges"
            },
            "High": {
                "Containment": "Isolate compromised accounts",
                "Recovery": "Full security audit and remediation",
                "NIST": "RS.AN-5: Processes are established to receive, analyze and respond to vulnerabilities",
                "ASD 8": "Daily backups"
            }
        },
        "Data Breach": {
            "Low": {
                "Containment": "Revoke exposed credentials",
                "Recovery": "Security monitoring",
                "NIST": "ID.RA-4: Potential business impacts and likelihoods are identified",
                "ASD 8": "Implement application control"
            },
            "Medium": {
                "Containment": "Restrict data access",
                "Recovery": "Data classification review",
                "NIST": "PR.DS-5: Protections against data leaks are implemented",
                "ASD 8": "Configure Microsoft Office macro settings"
            },
            "High": {
                "Containment": "Complete lockdown of affected systems",
                "Recovery": "Data loss assessment and notification",
                "NIST": "RS.CO-2: Incidents are reported consistent with response plan",
                "ASD 8": "Continuous vulnerability assessment and remediation"
            }
        }
    }
    # svae the sample ones incase it doesnt show
    with open('incidents.json', 'w') as f:
        json.dump(INCIDENTS, f, indent=2)

LOG_FILE = "incident_logs.json"

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
    
    # save it for user when they log
    log_entry = {
        "incident": incident_type,
        "severity": severity,
        "description": custom_desc if custom_desc else "No description provided",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # JSON format for logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return render_template('index.html', 
                          incidents=INCIDENTS,
                          response=response_data, 
                          selected=incident_type,
                          severity=severity, 
                          timeline=timeline,
                          description=custom_desc)

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE):
        return render_template('logs.html', logs=[])
    
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logs = []
    
    # dorting logs by timestamp 
    logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return render_template('logs.html', logs=logs)

@app.route('/download-report')
def download_report():
    try:
        path = generate_pdf_report()
        return send_file(path, as_attachment=True)
    except Exception as e:
        flash(f"Error generating report: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/clear-logs', methods=['POST'])
def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return redirect(url_for('logs'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', incidents=INCIDENTS, error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', incidents=INCIDENTS, error="Server error occurred"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)