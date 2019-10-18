from django.shortcuts import render
from django.urls import path

# Create your views here.
def index(request):
    message = "Welcome to Prowards"

    context = {
        "message":message,
    }

    return render(request,'wards/index.html',context)