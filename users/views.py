from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View

from django.views.decorators.csrf import csrf_exempt


from .models import User

class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    @csrf_exempt
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error_message': 'Email already exists'})
            elif User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error_message': 'Username already exists'})
            else:
                user = User.objects.create_user(email=email, username=username, password=password1)
                user.save()
                return redirect('/users/login/')
        else:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    @csrf_exempt
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

        if user.check_password(password):
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/users/login/')