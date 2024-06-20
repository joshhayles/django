from django.urls import path 
from reports.views import valuation_form, valuation_submission, purchase_report

app_name = 'reports'
urlpatterns = [
    path('valuation-form/', valuation_form, name='valuation_form'),
    path('valuation-submission/', valuation_submission, name='valuation_submission'),
    path('purchase-report/', purchase_report, name='purchase_report'),
]