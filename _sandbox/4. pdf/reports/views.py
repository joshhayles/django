from django.shortcuts import render, redirect
from django.http import HttpResponse
from .report_generator import create_report
import logging 

def valuation_form(request):
    # Render the valuation form template
    logging.info('valuation_form view called')
    return render(request, 'valuation_form.html')

def valuation_submission(request):
    # Handle the form submission and render the 'Purchase Report' page
    if request.method == 'POST':
        # Process the form data
        # ...

        # Render the 'Purchase Report' page
        return render(request, 'purchase_report.html')
    else:
        # Redirect to the valuation form if the request is not POST
        return redirect('reports:valuation_form')

def purchase_report(request):
    # Handle the 'Purchase Report' button click
    # You can add your Stripe checkout integration here
    return render(request, 'purchase_report.html')

def generate_pdf_view(request):
    if request.method == 'POST' or request.GET.get('session_id'):
        # generate the PDF
        data = {
            'prepared_by': 'Josh Hayles',
            'listing_date': '04/24/24 at 12:58 pm',
            'address': '319 Woodway Drive',
            'mls': '89169834',
            'dom': '19',
            'cdom': '68',
            'list_price': '$439,000',
            'list_date': '01/18/2023',
            'status': 'Sold'
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="property_report.pdf"'
        create_report(response, data)
        return response
    
    # If it's a GET request, just show the button
    return render(request, 'success.html')