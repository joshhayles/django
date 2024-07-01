from django.urls import path 
from reports.views import evaluation_form, evaluation_submission, purchase_report, GeneratePDFView

app_name = 'reports'
urlpatterns = [
    path('evaluation-form/', evaluation_form, name='evaluation_form'),
    path('evaluation-submission/', evaluation_submission, name='evaluation_submission'),
    path('purchase-report/', purchase_report, name='purchase_report'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate_pdf'),
]