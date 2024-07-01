from django.views.generic import TemplateView
from django.urls import reverse

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evaluation_form_url'] = reverse('reports:evaluation_form')
        return context