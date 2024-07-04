# views.py

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User 
from importlib import import_module
import stripe

class HomePageView(TemplateView):
    template_name = 'home.html'

User = get_user_model()
class SuccessView(TemplateView):
    template_name = 'success.html'

    def dispatch(self, request, *args, **kwargs):
        print(f"SuccessView dispatch - Method: {request.method}")
        print(f"SuccessView dispatch - User authenticated: {request.user.is_authenticated}")
        print(f"SuccessView dispatch - Username: {request.user.username}")
        print(f"SuccessView dispatch - Session key: {request.session.session_key}")
        print(f"SuccessView dispatch - GET params: {request.GET}")
        print(f"SuccessView dispatch - POST params: {request.POST}")
        
        # Try to restore the session
        django_session = request.GET.get('django_session')
        if django_session and not request.user.is_authenticated:
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore(django_session)
            user_id = session.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    login(request, user)
                    print(f"Session restored for user: {user.username}")
                except User.DoesNotExist:
                    print(f"User with id {user_id} not found")
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        print(f"SuccessView GET - Session ID: {session_id}")
        print(f"SuccessView GET - User authenticated: {request.user.is_authenticated}")
        print(f"SuccessView GET - Username: {request.user.username}")
        print(f"SuccessView GET - Session key: {request.session.session_key}")
        
        if not request.user.is_authenticated:
            print("User not authenticated in SuccessView GET method")
            return redirect(reverse('login'))
        
        context = {'session_id': session_id}
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        session_id = request.POST.get('session_id')
        print(f"SuccessView POST - Session ID: {session_id}")
        print(f"SuccessView POST - User authenticated: {request.user.is_authenticated}")
        print(f"SuccessView POST - Username: {request.user.username}")
        print(f"SuccessView POST - Session key: {request.session.session_key}")
        
        if not request.user.is_authenticated:
            print("User not authenticated in SuccessView POST method")
            return redirect(reverse('login'))
        
        return redirect(reverse('reports:generate_pdf') + f'?session_id={session_id}')

class CancelledView(TemplateView):
    template_name = 'cancelled.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@login_required
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create a price object
            price = stripe.Price.create(
                unit_amount=2700,  # Amount in cents
                currency='usd',
                product_data={
                    'name': 'Protest Report',
                },
            )
            # Include the session key in the success URL
            success_url = domain_url + reverse('payments:success') + f'?session_id={{CHECKOUT_SESSION_ID}}&django_session={request.session.session_key}'
            checkout_session = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=domain_url + reverse('payments:cancelled'),
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    }
                ],
                client_reference_id=request.user.id,  # Add this line to associate the checkout session with the user
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body 
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None 

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful")

    return HttpResponse(status=200)