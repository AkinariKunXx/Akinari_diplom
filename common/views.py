from django.contrib.auth import logout
from django.shortcuts import render, redirect
from common.models import Order

def index(request):
    return render(request, 'index.html')

def game_pc(request):
    return render(request, 'game_pc.html')

def work_pc(request):
    return render(request, 'work_pc.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def services(request):
    return render(request, 'services.html')

def about_us(request):
    return render(request, 'about_us.html')