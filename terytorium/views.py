from django.views.generic import ListView
from terytorium.models import Woj

class Home(ListView):
    template_name = 'woj.html'
    model = Woj
    context_object_name = 'wojs'
