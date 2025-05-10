from fpdf import FPDF
from datetime import datetime
import os

def generate_timeline(response):
    return [
        {"step": "Detect", "duration": "0-15 mins"},
        {"step": "Contain - " + response.get("Containment", ""), "duration": "15-30 mins"},
        {"step": "Recover - " + response.get("Recovery", ""), "duration": "30-60 mins"},
        {"step": "Post-Review", "duration": "60-90 mins"}
    ]

def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Incident Report", ln=True, align='C')
    pdf.cell(200, 10, txt="Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M"), ln=True)

    if os.path.exists("log.txt"):
        with open("log.txt") as f:
            for line in f:
                pdf.multi_cell(0, 10, txt=line)
    
    filename = "incident_report.pdf"
    pdf.output(filename)
    return filename
