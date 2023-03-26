import pdfkit
from flask import render_template


def generate_pdf_doc(cv_data: dict) -> bytes:
    # Render the HTML template with the CV data
    html = render_template('./template.html', **cv_data)

    # Create a PDF from the rendered HTML
    pdf = pdfkit.from_string(html, False)

    return pdf
