from django.shortcuts import render
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'base/about.html'

class Error404View(TemplateView):
    template_name = 'base/error_404.html'
