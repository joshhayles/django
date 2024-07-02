import json, statistics
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, PageTemplate, NextPageTemplate, Spacer, Image, PageBreak, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib import colors
from datetime import datetime
import os, requests, logging
from io import BytesIO
from django.conf import settings
from django.contrib.staticfiles import finders
from PIL import Image as PILImage
from .models import Property

# Image compression
def compress_image(image_path, quality=60, max_size=(300,300)):
    with PILImage.open(image_path) as img:
        img.thumbnail(max_size)
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG', quality=quality, optimize=True)
        img_buffer.seek(0)
    return img_buffer

# Register font
def get_font_path(font_name):
    # Try the production static root first
    font_path = os.path.join(settings.STATIC_ROOT, 'fonts', font_name)
    if os.path.exists(font_path):
        return font_path
    
    # If not found, try the development static directories
    for static_dir in settings.STATICFILES_DIRS:
        font_path = os.path.join(static_dir, 'fonts', font_name)
        if os.path.exists(font_path):
            return font_path
    
    # If still not found, raise an error
    raise FileNotFoundError(f"{font_name} not found in static directories")

# Register font
try:
    regular_font_path = get_font_path('Inter-Regular.ttf')
    bold_font_path = get_font_path('Inter-Bold.ttf')
    pdfmetrics.registerFont(TTFont('Inter-Regular', regular_font_path))
    pdfmetrics.registerFont(TTFont('Inter-Bold', bold_font_path))
    logging.info(f"Font registered successfully from: {regular_font_path} and {bold_font_path}")
except FileNotFoundError as e:
    logging.info(f"Error: {str(e)}")

def format_price(price):
    if isinstance(price, (int, float)):
        return f"${price:,.0f}"
    elif isinstance(price, str):
        try:
            clean_price = float(price.replace('$', '').replace(',', ''))
            return f"${clean_price:,.0f}"
        except ValueError:
            return price 
    else:
        return 'N/A'

def create_table_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Inter-Regular'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Reduced font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), '#EEEEEE'),
        ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Reduced font size
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, '#000000')
    ])

def subject_home(elements, user_data):
    logging.info("Entering subject_home function")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('SubjectTitle', parent=styles['Heading2'], fontName='Inter-Regular', fontSize=14, spaceAfter=12, alignment=1)
    elements.append(Paragraph('Subject Home', title_style))
    logging.info("Added 'Subject Home' title to elements")
    
    if user_data:
        logging.info("User data is not empty, creating table")
        table_data = [
            ['Address', 'Sq Ft', 'Year Built', 'Beds', 'Baths'],
            [
                user_data.get('address', 'N/A'),
                str(user_data.get('square_footage', 'N/A')),
                str(user_data.get('year_built', 'N/A')),
                str(user_data.get('bedrooms', 'N/A')),
                str(user_data.get('bathrooms', 'N/A'))
            ]
        ]
        logging.info("Table data:", table_data)

        table = Table(table_data, colWidths=[2.1*inch, 1.075*inch, 1.075*inch, 1.075*inch, 1.075*inch])
        table.setStyle(create_table_style())
        logging.info("Table created and styled")

        elements.append(table)
        logging.info("Table added to elements")
    else:
        logging.info("No user data available, adding placeholder text")
        elements.append(Paragraph("No subject home data available", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    logging.info("Added spacer after subject home section")
    logging.info("Exiting subject_home function")

def comparable_homes(elements, homes_data):
    logging.info("Entering comparable_homes function")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ComparableTitle', parent=styles['Heading2'], fontName='Inter-Regular', fontSize=14, spaceAfter=12, alignment=1)
    elements.append(Paragraph('Comparable Homes', title_style))
    
    if homes_data and len(homes_data) >= 3:
        # limit homes to maximum of 6
        homes_to_display = homes_data[:6]

        table_data = [['Address', 'Sold Price', 'Sq Ft', 'Year Built', 'Beds', 'Baths', 'Sold Date']]
        for home in homes_to_display:
            table_data.append([
                home.get('address', 'N/A'),
                format_price(home.get('sold_price', 'N/A')),
                str(home.get('square_footage', 'N/A')),
                str(home.get('year_built', 'N/A')),
                str(home.get('bedrooms', 'N/A')),
                str(home.get('bathrooms', 'N/A')),
                home.get('Sold Date', 'N/A')
            ])

        logging.info(f"Table data: {table_data}")

        if len(table_data) > 1:  # Check if we have any data rows besides the header
            try:
                table = Table(table_data, colWidths=[2.1*inch, 0.9*inch, 0.7*inch, 0.8*inch, 0.5*inch, 0.5*inch, 0.9*inch])
                table.setStyle(create_table_style())
                elements.append(table)
                logging.info("Table created and added to elements")
            except Exception as e:
                logging.error(f"Error creating table: {str(e)}")
                elements.append(Paragraph("Error creating comparable homes table", styles['Normal']))
        else:
            logging.warning("No data rows in table_data")
            elements.append(Paragraph("No comparable homes data available", styles['Normal']))
    else:
        logging.warning("No homes data available")
        elements.append(Paragraph("No comparable homes data available", styles['Normal']))
    
    logging.info("Exiting comparable_homes function")
    return homes_to_display

def create_summary_graph(homes_data):
    # Calculate values
    sold_prices = [float(home['sold_price']) for home in homes_data if 'sold_price' in home]
    if not sold_prices:
        return None
    avg_price = sum(sold_prices) / len(sold_prices)
    min_price = min(sold_prices)
    max_price = max(sold_prices)
    median_price = statistics.median(sold_prices)

    # Create drawing
    doc_width = letter[0] - inch  # subtract margins
    drawing_width = doc_width
    drawing_height = 200
    drawing = Drawing(drawing_width, drawing_height)

    # Create chart
    chart_width = drawing_width * 0.80  # 80% of drawing width
    bc = VerticalBarChart()
    bc.x = (drawing_width - chart_width) / 2  # Center the chart
    bc.y = 40
    bc.height = 150
    bc.width = chart_width
    bc.data = [[avg_price], [median_price], [min_price], [max_price]]
    bc.bars.fillColor = None
    bc.bars[0].fillColor = colors.steelblue
    bc.bars[1].fillColor = colors.limegreen
    bc.bars[2].fillColor = colors.indianred
    bc.bars[3].fillColor = colors.lightgreen
    bc.barSpacing = 6
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max_price * 1.1
    bc.valueAxis.valueStep = max_price / 5
    bc.categoryAxis.labels.boxAnchor = 'n'
    bc.categoryAxis.labels.dy = -10
    bc.categoryAxis.tickDown = 0
    bc.categoryAxis.visibleTicks = False
    bc.categoryAxis.visibleLabels = False

    drawing.add(bc)

    # Calculate bar positions
    num_bars = len(bc.data)
    total_bar_space = bc.width - (bc.barSpacing * (num_bars - 1))
    bar_width = total_bar_space / num_bars
    
    # Function to calculate x-coordinate for the center of each bar
    def get_bar_center_x(i):
        return bc.x + (i * (bar_width + bc.barSpacing)) + (bar_width / 2)

    # Add value labels inside bars
    for i, value in enumerate([avg_price, median_price, min_price, max_price]):
        x = get_bar_center_x(i)
        bar_height = (value / bc.valueAxis.valueMax) * bc.height
        y = bc.y + (bar_height / 2)
        label = String(x, y, f'${value:,.0f}')
        label.fontName = "Inter-Regular"
        label.fontSize = 12
        label.textAnchor = 'middle'
        label.fillColor = colors.black
        drawing.add(label)

    # Add category labels below the chart
    categories = ['Avg Sales Price', 'Median Sales Price', 'Min Sales Price', 'Max Sales Price']
    
    for i, category in enumerate(categories):
        x = get_bar_center_x(i)
        y = bc.y - 20  # Adjust this value if needed to fine-tune vertical positioning
        label = String(x, y, category)
        label.fontName = "Inter-Regular"
        label.fontSize = 8
        label.textAnchor = 'middle'
        drawing.add(label)

    return drawing

def create_home_table(homes, placeholder_image, title_style, normal_style):
    logging.info(f"Creating home table for {len(homes)} homes")

    # create bold style
    bold_style = ParagraphStyle('BoldStyle', parent=normal_style, fontName='Inter-Bold')

    data = []
    for home in homes:
        col_data = [
            [placeholder_image],
            [Paragraph(f"<b>{home.get('address', 'N/A')}</b>", title_style)],
            [Paragraph(f"<b>MLS #:</b> {home.get('MLS', 'N/A')}", normal_style)],
            [Paragraph(f"<b>List Price:</b> {format_price(home.get('list_price', 'N/A'))}", normal_style)],
            [Paragraph(f"<b>LP per SF:</b> {home.get('lp_sf', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Sold Price:</b> {format_price(home.get('sold_price', 'N/A'))}", bold_style)],
            [Paragraph(f"<b>SP per SF:</b> {home.get('sp_sf', 'N/A')}", bold_style)],
            [Paragraph(f"<b>Square Feet:</b> {home.get('square_footage', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Year Built:</b> {home.get('year_built', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Beds:</b> {home.get('bedrooms', 'N/A')} <b>Baths:</b> {home.get('bathrooms', 'N/A')}", normal_style)],
            [Paragraph(f"<b>DOM:</b> {home.get('DOM', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Status:</b> {home.get('Status', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Sold Date:</b> {home.get('Sold Date', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Subdivision:</b> {home.get('Subdivision', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Lot Size:</b> {home.get('Lot Size', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Stories:</b> {home.get('Stories', 'N/A')}", normal_style)],
            [Paragraph(f"<b>Pool:</b> {home.get('Pool', 'N/A')}", normal_style)]
        ]
        data.append(col_data)
    
    # Pad with empty columns if less than 3 homes
    while len(data) < 3:
        data.append([[]] * 14)

    logging.info("Creating table")
    table = Table(list(zip(*data)), colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.lightgrey),
    ]))
    logging.info("Table created successfully")
    return table

# Define the main function
def three_column_view(homes_data):
    logging.info("Entering three_column_view function")
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ColumnTitle', parent=styles['Heading3'], fontName='Inter-Regular', fontSize=10, spaceAfter=6)
    normal_style = ParagraphStyle('ColumnNormal', parent=styles['Normal'], fontName='Inter-Regular', fontSize=8, leading=10)

    # Use Django's static file finder to get the absolute path of the image
    logging.info("Finding placeholder image")
    image_path = finders.find('img/img1.webp')
    if image_path is None:
        logging.error("Placeholder image not found")
        placeholder_image = Paragraph("Image not available", normal_style)
    else:
        logging.info(f"Placeholder image found at {image_path}")
        try:
            img_buffer = compress_image(image_path, quality=60, max_size=(300, 300))
            placeholder_image = Image(img_buffer, width=2*inch, height=1.5*inch)
        except Exception as e:
            logging.error(f"Error compressing image: {str(e)}")
            placeholder_image = Paragraph("Image compression failed", normal_style)
    
    result_elements = []

    # First 3 homes on the second page
    logging.info("Creating table for first 3 homes")
    result_elements.append(create_home_table(homes_data[:3], placeholder_image, title_style, normal_style))
    result_elements.append(Spacer(1, 0.3 * inch))

    # If there are more than 3 homes, add a page break and create another table
    if len(homes_data) > 3:
        logging.info("Creating table for additional homes")
        result_elements.append(PageBreak())
        result_elements.append(Spacer(1, 0.25*inch))
        result_elements.append(Paragraph("Additional Comparable Homes", styles['Title']))
        result_elements.append(Spacer(1, 0.2 * inch))
        result_elements.append(create_home_table(homes_data[3:], placeholder_image, title_style, normal_style))

    logging.info("Exiting three_column_view function")
    return result_elements

def header(canvas, doc):
    canvas.saveState()
    canvas.setFont('Inter-Regular', 9)
    canvas.drawString(inch, doc.pagesize[1] - 0.5*inch, f"Presented by: Josh Hayles | Licensed Realtor")
    canvas.drawString(inch, doc.pagesize[1] - 0.7*inch, f"{datetime.now().strftime('%B %d, %Y')}")
    canvas.line(inch, doc.pagesize[1] - 0.75*inch, doc.width + doc.leftMargin - inch, doc.pagesize[1] - 0.75*inch)
    canvas.restoreState()

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Inter-Regular', 9)
    footer_text = "This is a Comparative Market Analysis for Property Tax purposes. It is NOT an Appraisal or opinion of value. Copyright: Data provided by the Houston Association of REALTORS© (HAR) 2024. All rights reserved. Information is believed to be accurate but is not guaranteed."
    footer_style = ParagraphStyle('footer', fontName='Inter-Regular', fontSize=9, leading=11)
    p = Paragraph(footer_text, footer_style)
    w, h = p.wrap(6 * inch, inch)  # 6 inch width, 1 inch height
    p.drawOn(canvas, inch, 0.5 * inch)
    canvas.restoreState()

def create_pdf(homes_data, user_data):
    # importing Property model at the top, and I can pass property_instance as an argument to use in the report generation process

    logging.info("Starting PDF creation")
    logging.info(f"Original number of homes: {len(homes_data)}")

    # Limit the number of homes
    if len(homes_data) < 3:
        logging.warning("Not enough homes data for report")
        return None
    elif len(homes_data) > 6:
        homes_data = homes_data[:6]
        logging.info("Limited homes data to 6 homes")

    logging.info(f"Final number of homes for report: {len(homes_data)}")
    logging.info(f"homes_data: {json.dumps(homes_data, indent=2)}")
    logging.info(f"user_data: {json.dumps(user_data, indent=2)}")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontName='Inter-Regular', alignment=1, spaceAfter=12)

    try:
        # First page content
        elements.append(Spacer(1, 0.05*inch)) # Reduced space before first title
        elements.append(Paragraph("Property Tax Protest Report", title_style))
        elements.append(Spacer(1, 0.1*inch))
        
        displayed_homes = comparable_homes(elements, homes_data)
        elements.append(Spacer(1, 0.1*inch))

        if user_data:
            subject_home(elements, user_data)
        else:
            elements.append(Paragraph("No subject home data available", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

        # use displayed homes for graph
        graph = create_summary_graph(displayed_homes)
        if graph:
            elements.append(graph)
        else:
            elements.append(Paragraph("Unable to generate summary graph", styles['Normal']))

        # Second page with three-column view
        elements.append(NextPageTemplate('other_pages'))
        elements.append(PageBreak())
        elements.append(Spacer(1, 0.25*inch)) # space for header
        elements.append(Paragraph("Comparable Homes", title_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(NextPageTemplate('other_pages'))
        three_column_view_elements = three_column_view(homes_data)
        elements.extend(three_column_view_elements)

        # Create page templates
        first_page_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.5*inch, id='first_page')
        other_pages_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.5*inch, id='other_pages')

        first_page_template = PageTemplate(id='first_page', frames=[first_page_frame], onPage=header, onPageEnd=footer)
        other_pages_template = PageTemplate(id='other_pages', frames=[other_pages_frame], onPage=header, onPageEnd=footer)

        doc.addPageTemplates([first_page_template, other_pages_template])

        doc.build(elements)
        logging.info("PDF creation completed successfully!")

    except Exception as e:
        logging.error(f"Error during PDF creation: {str(e)}")
        logging.error(f"Number of elements: {len(elements)}")
        for i, element in enumerate(elements):
            logging.error(f"Element {i}: {type(element)}")
        raise

    pdf = buffer.getvalue()
    buffer.close()
    return pdf