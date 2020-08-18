from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.reverse import lazy

from frontend.forms import EventUserForm

class EventListView(TemplateView):
    template_name = 'frontend/list-events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_user_form"] = EventUserForm()
        return context

class SimpleView(TemplateView):
    template_name = 'frontend/simple.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_user_form"] = EventUserForm()
        context["url"] = lazy('event-list',request=self.request)
        return context
    