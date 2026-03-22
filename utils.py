import os
from openai import OpenAI
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ---------------- GROQ CLIENT ----------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- AI FUNCTION ----------------
def ask_ai(prompt):
    if len(prompt) > 12000:
        prompt = prompt[:12000] + "\n\n(Summarize this truncated content)"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ updated model
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# ---------------- PDF FUNCTION ----------------
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text

# ---------------- PDF GENERATION FUNCTION ----------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch

def create_pdf(input_text, output_text, filename="ai_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # ---------------- CUSTOM STYLES ----------------
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=15   # line spacing
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        leftIndent=15,
        spaceAfter=6
    )

    content = []

    # ---------------- TITLE ----------------
    content.append(Paragraph("AI SMART ACADEMIC ASSISTANT REPORT", title_style))

    # ---------------- INPUT ----------------
    content.append(Paragraph("■ USER INPUT (Your Question):", heading_style))
    content.append(Paragraph(input_text, body_style))
    content.append(Spacer(1, 12))

    # ---------------- OUTPUT ----------------
    content.append(Paragraph("■ AI RESPONSE:", heading_style))

    # 🔥 Handle bullet formatting properly
    if "*" in output_text or "-" in output_text:
        lines = output_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("*") or line.startswith("-"):
                clean_line = line.replace("*", "").replace("-", "").strip()
                content.append(Paragraph(f"• {clean_line}", bullet_style))
            else:
                content.append(Paragraph(line, body_style))
    else:
        content.append(Paragraph(output_text, body_style))

    content.append(Spacer(1, 12))

    # ---------------- FOOTER ----------------
    content.append(Paragraph("<i>Generated using AI Academic Assistant</i>", styles['Italic']))

    # Build PDF
    doc.build(content)

    return filename
