from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'woj.html'
    context_object_name = 'home'
