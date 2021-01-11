from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


class IndexView(TemplateView):
    template_name = 'index.html'
