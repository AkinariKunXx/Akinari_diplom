from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from common.models import Booking
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
def index(request):
    return render(request, 'index.html')

def game_pc(request):
    return render(request, 'game_pc.html')

def work_pc(request):
    return render(request, 'work_pc.html')

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def services(request):
    return render(request, 'services.html')

def about_us(request):
    return render(request, 'about_us.html')


@login_required
def profile(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    upcoming_bookings = user_bookings.filter(start_date__gte=datetime.now().date())
    past_bookings = user_bookings.filter(start_date__lt=datetime.now().date())

    if request.method == 'POST':
        # Обновление профиля
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.bio = request.POST.get('bio', profile.bio)

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, 'profile.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Проверка валидности данных
        if not all([username, email, password1, password2, first_name, last_name]):
            return JsonResponse({
                'success': False,
                'errors': 'Все поля обязательны для заполнения'
            })

        if password1 != password2:
            return JsonResponse({
                'success': False,
                'errors': 'Пароли не совпадают'
            })

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'errors': 'Пользователь с таким именем уже существует'
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'errors': 'Пользователь с таким email уже существует'
            })

        try:
            # Создаем нового пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return JsonResponse({
                'success': True,
                'message': 'Регистрация успешна'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': str(e)
            })

    return JsonResponse({
        'success': False,
        'errors': 'Метод не поддерживается'
    })