from django.shortcuts import render
from django.views.generic import TemplateView, FormView, RedirectView

class AboutView(TemplateView):
    template_name = 'base/about.html'
