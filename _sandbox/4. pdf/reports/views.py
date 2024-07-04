from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from .generate_report import create_pdf
from .models import Property
import json, os
import logging 

def evaluation_form(request):
    # Render the evaluation form template
    logging.info('evaluation_form view called')
    return render(request, 'evaluation_form.html')

def evaluation_submission(request):
    if request.method == 'POST':
        logging.info("POST data received:")
        for key, value in request.POST.items():
            logging.info(f"{key}: {value}")

        try:
            address = request.POST.get('property-address')
            if not address:
                raise ValueError("Property Address is required")
            
            # process square footage
            square_footage = request.POST.get('square-footage')
            if square_footage == 'less-than-2000':
                square_feet = 1999
            elif square_footage == 'above-4000':
                square_feet = 4001
            else:
                # take lower end of range
                square_feet = int(square_footage.split('-')[0])

            property_data = Property(
                address=address,
                proposed_market_value=request.POST.get('proposed-market-value') or None,
                property_type=request.POST.get('property-type') or None,
                square_feet=square_feet,
                year_built=request.POST.get('year-built') or None,
                private_pool=request.POST.get('private-pool') == 'yes'
            )
            property_data.save()
            logging.info(f"Property saved successfully: {property_data}")
            return render(request, 'purchase_report.html')
        except Exception as e:
            logging.error(f"Error saving property: {str(e)}")
            return render(request, 'error.html', {'error_message': str(e)})
    else:
        return redirect('reports:evaluation_form')

def purchase_report(request):
    # Handle the 'Purchase Report' button click
    # You can add your Stripe checkout integration here
    return render(request, 'purchase_report.html')

class GeneratePDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logging.info(f"GeneratePDFView GET method called. User authenticated: {request.user.is_authenticated}")
        logging.info(f"Username: {request.user.username}")
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

            # Load most recent Property instance
            latest_property = Property.objects.latest('id') # id should auto-increment
            logging.info(f"Retrieved latest property information: {latest_property}")

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