from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # This line logs in the user
        return valid

@login_required
def retrieve_user_information(request):
    # get logged-in user instance
    user = request.user
    # pass information as part of the context data
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'address': user.address,
        'city': user.city,
        'state': user.state,
        'zip': user.zip,
    }
    return render(request, 'evaluation_form.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
        
        elif request.POST.get('remove_picture') == 'true':
            request.user.profile_picture = None 
            request.user.save()
            
        return redirect('profile')
    return render(request, 'profile.html', {'user': request.user})


