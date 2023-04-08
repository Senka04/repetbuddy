from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'page1/index.html') # представляем, что мы уже в templates
def registration(request):
    return render(request, 'page1/registration.html') # представляем, что мы уже в templates
def login(request):
    return render(request, 'page1/login.html') # представляем, что мы уже в templates
# Create your views here.
