from django.urls import path 
from reports.views import valuation_form, valuation_submission, purchase_report, generate_pdf_view

app_name = 'reports'
urlpatterns = [
    path('valuation-form/', valuation_form, name='valuation_form'),
    path('valuation-submission/', valuation_submission, name='valuation_submission'),
    path('purchase-report/', purchase_report, name='purchase_report'),
    path('generate-pdf/', generate_pdf_view, name='generate_pdf'),
    path('report-success/', generate_pdf_view, name='report-success'),
]