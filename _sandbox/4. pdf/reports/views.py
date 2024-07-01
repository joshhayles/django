from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from .generate_report import create_pdf
import json, os
import logging 

def evaluation_form(request):
    # Render the evaluation form template
    logging.info('evaluation_form view called')
    return render(request, 'evaluation_form.html')

def evaluation_submission(request):
    # Handle the form submission and render the 'Purchase Report' page
    if request.method == 'POST':
        # Process the form data
        # ...

        # Render the 'Purchase Report' page
        return render(request, 'purchase_report.html')
    else:
        # Redirect to the valuation form if the request is not POST
        return redirect('reports:evaluation_form')

def purchase_report(request):
    # Handle the 'Purchase Report' button click
    # You can add your Stripe checkout integration here
    return render(request, 'purchase_report.html')

class GeneratePDFView(View):
    def get(self, request, *args, **kwargs):
        try:
            logging.info("GeneratePDFView GET method called")
            
            # Load homes data
            with open(os.path.join('reports', 'data', 'homes.json'), 'r') as file:
                homes_data = json.load(file)
            logging.info(f"Loaded homes_data: {len(homes_data)} items")
            
            # Load user data
            with open(os.path.join('reports', 'data', 'user_info.json'), 'r') as file:
                user_data = json.load(file)
            logging.info("User data loaded successfully")

            # Generate PDF
            pdf = create_pdf(homes_data, user_data)

            if pdf is None:
                return HttpResponse("Unable to generate PDF: Not enough comparable homes", status=400)

            # Create the HttpResponse object with PDF mime type
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="property_analysis_report.pdf"'

            logging.info("PDF generated and response created successfully")
            return response

        except FileNotFoundError as e:
            logging.error(f"File not found: {str(e)}")
            return HttpResponse(f"Error: Required data files not found. {str(e)}", status=500)
        
        except Exception as e:
            logging.error(f"An error occurred while generating the PDF: {str(e)}")
            return HttpResponse(f"An error occurred while generating the PDF: {str(e)}", status=500)