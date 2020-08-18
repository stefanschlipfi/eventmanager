from django.shortcuts import render
from django.views.generic import TemplateView
# Create your view
# s here.

class EventListView(TemplateView):
    template_name = 'frontend/list-events.html'