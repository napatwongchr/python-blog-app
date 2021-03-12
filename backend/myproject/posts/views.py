from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def post_list(request):
    return HttpResponse("Hello, this is posts app")