from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'login/index.html')


def register(request):
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        date_of_birth = request.POST['date_of_birth']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name=first_name, last_name=last_name, email=email, date_birth=date_of_birth,
                            password=pw_hash)
        user_list = User.objects.filter(email=email)
        user = user_list[0]
        request.session['user'] = user.id
        request.session['logged_in'] = True
        return redirect('/success')


def success(request):
    if 'logged_in' in request.session:
        return render(request, 'login/success.html')
    else:
        return redirect('/')


def login(request):
    if 'logged_in' in request.session:
        return redirect('/success')

    errors = User.objects.user_login(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        user_list = User.objects.filter(email=email)
        user = user_list[0]
        request.session['user'] = user.id
        request.session['logged_in'] = True
        return redirect('/success')


def logout(request):
    request.session.flush()
    return redirect('/')
