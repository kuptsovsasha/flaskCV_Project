from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf(cv_data, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Set up styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', fontSize=16, leading=20))
    styles.add(ParagraphStyle(name='Subheader', fontSize=14, leading=18))

    # Build the PDF elements
    elements = []

    # Personal information
    elements.append(Paragraph(cv_data["personal_info"]["full_name"], styles["Header"]))
    elements.append(Paragraph(cv_data["personal_info"]["email"], styles["Normal"]))
    elements.append(Paragraph(cv_data["personal_info"]["phone"], styles["Normal"]))
    if "linkedin" in cv_data["personal_info"]:
        elements.append(Paragraph(cv_data["personal_info"]["linkedin"], styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Professional summary
    if cv_data["summary"]:
        elements.append(Paragraph("Professional Summary", styles["Subheader"]))
        elements.append(Paragraph(cv_data["summary"], styles["Normal"]))
        elements.append(Spacer(1, 20))

    # Work experience
    if cv_data["work_experience"]:
        elements.append(Paragraph("Work Experience", styles["Subheader"]))
        for experience in cv_data["work_experience"]:
            elements.append(Paragraph(f"{experience['job_title']} at {experience['company']} ({experience['start_date']} - {experience['end_date']})", styles["Normal"]))
            elements.append(Paragraph(experience["description"], styles["Normal"]))
            elements.append(Spacer(1, 10))
        elements.append(Spacer(1, 20))

    # Education
    if cv_data["education"]:
        elements.append(Paragraph("Education", styles["Subheader"]))
        for edu in cv_data["education"]:
            elements.append(Paragraph(f"{edu['degree']} - {edu['institution']} ({edu['year']})", styles["Normal"]))
            elements.append(Spacer(1, 10))
        elements.append(Spacer(1, 20))

    # Skills
    if cv_data["skills"]:
        elements.append(Paragraph("Skills", styles["Subheader"]))
        skills_table = Table([cv_data["skills"][i:i + 3] for i in range(0, len(cv_data["skills"]), 3)])
        skills_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(skills_table)
        elements.append(Spacer(1, 20))

    # Other sections (projects, awards, languages, volunteer work) can be added similarly

    # Build
    doc.build(elements)

    # Get the PDF content as a bytes object
    pdf_content = buffer.getvalue()

    # Close the buffer
    buffer.close()

    return pdf_content
