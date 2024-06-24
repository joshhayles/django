# payments/urls.py

from django.urls import path
from .views import stripe_config, create_checkout_session, stripe_webhook, HomePageView, SuccessView, CancelledView

app_name = 'payments'

urlpatterns = [
    path('config/', stripe_config, name='stripe_config'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelledView.as_view(), name='cancelled'),
    path('', HomePageView.as_view(), name='home'),
]
