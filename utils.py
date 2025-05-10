from fpdf import FPDF
from datetime import datetime
import os
import random

def generate_timeline(response):
    # More detailed and realistic timeline
    return [
        {"step": "Detection", "duration": "T+0 mins"},
        {"step": "Triage", "duration": "T+5 mins"},
        {"step": "Containment - " + response.get("Containment", ""), "duration": "T+15 mins"},
        {"step": "Recovery - " + response.get("Recovery", ""), "duration": "T+30 mins"},
        {"step": "Implementation of " + response.get("NIST", ""), "duration": "T+45 mins"},
        {"step": "Post-Incident Review", "duration": "T+60 mins"}
    ]

def generate_pdf_report():
    # Create custom cybersecurity-themed PDF
    pdf = FPDF()
    pdf.set_author("Cybersecurity Incident Response Team")
    pdf.set_title("Incident Response Report")
    
    # Add cover page
    pdf.add_page()
    pdf.set_fill_color(10, 25, 41)  # Dark blue background
    pdf.rect(0, 0, 210, 297, 'F')  # Fill page with background color
    
    # Add header
    pdf.set_font("Helvetica", 'B', 24)
    pdf.set_text_color(0, 242, 255)  # Cyber blue
    pdf.cell(0, 30, "", ln=True)  # Space at top
    pdf.cell(0, 20, "CYBERSECURITY", ln=True, align='C')
    pdf.cell(0, 20, "INCIDENT REPORT", ln=True, align='C')
    
    # Add timestamp
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, "", ln=True)  # Space
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.cell(0, 10, f"Reference ID: IR-{random.randint(10000, 99999)}", ln=True, align='C')
    
    # Content page
    pdf.add_page()
    pdf.set_fill_color(10, 25, 41)  # Dark blue background
    pdf.rect(0, 0, 210, 297, 'F')  # Fill page with background color
    
    # Add header for content
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 20, "INCIDENT DETAILS", ln=True, align='L')
    
    # Add incident logs
    pdf.set_font("Helvetica", '', 11)
    pdf.set_text_color(220, 220, 220)  # Light gray for content
    
    if os.path.exists("log.txt"):
        with open("log.txt") as f:
            pdf.set_fill_color(15, 40, 60)  # Slightly lighter blue for sections
            y_position = pdf.get_y()
            
            for i, line in enumerate(f):
                # Create a box for each log entry
                entry_height = 40  # Approximate height for entry
                pdf.rect(10, y_position, 190, entry_height, 'F')
                
                # Add content
                pdf.set_xy(15, y_position + 5)
                pdf.set_font("Helvetica", 'B', 11)
                pdf.cell(0, 10, f"Log Entry #{i+1}", ln=True)
                
                pdf.set_font("Helvetica", '', 10)
                pdf.multi_cell(180, 7, line)
                
                y_position += entry_height + 10
                
                # Add page if needed
                if y_position > 250:
                    pdf.add_page()
                    pdf.set_fill_color(10, 25, 41)  # Background
                    pdf.rect(0, 0, 210, 297, 'F')
                    y_position = 20
    else:
        pdf.cell(0, 10, "No incident logs available", ln=True)
    
    # Add security classification footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(0, 242, 255)
    pdf.cell(0, 10, "CONFIDENTIAL - INTERNAL USE ONLY", align='C')
    
    filename = f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    return filename