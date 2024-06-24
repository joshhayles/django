from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(response, data):
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']

    # Title
    elements.append(Paragraph("3-Up Comparison", title_style))
    elements.append(Paragraph(f"Prepared By: {data['prepared_by']}", normal_style))
    elements.append(Paragraph(f"Listings as of {data['listing_date']}", normal_style))

    # Property Details Table
    property_data = [
        ["Address", "MLS #", "DOM", "CDOM", "List Price", "List Date", "Status"],
        [data['address'], data['mls'], data['dom'], data['cdom'], data['list_price'], data['list_date'], data['status']],
        # Add more rows as needed
    ]

    property_table = Table(property_data)
    property_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(property_table)

    # Add more elements (tables, paragraphs) as needed

    # Build the PDF
    doc.build(elements)