import pprint
from django.shortcuts import render, redirect
# from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

from .forms import UserCustomChangeForm, UserCustomCreationForm

# Create your views here.
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            messages.info(request, f'{user.username}님, 회원가입 성공!')
            return redirect('boards:index')
        messages.warning(request, '양식을 다시 확인해주세요.')
    else:
        user_form = UserCustomCreationForm()
    context = {'user_form': user_form}
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            messages.info(request, f'{user.username}님, 로그인 성공!')
            return redirect('boards:index')
    else:
        login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('boards:index')

@login_required
# @require_http_methods(["POST"])
@require_POST
def delete(request):
    request.user.delete()
    return redirect('boards:index')
  
# @login_required
# def delete(request):
#     if request.method == 'POST':
#         request.user.delete()
#     return redirect('boards:index')

@require_http_methods(["GET", "POST"])
def update(request):
    # user_form = UserChangeForm()
    if request.method == 'POST':
        user_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('boards:index')
    else:
        user_form = UserCustomChangeForm(instance=request.user)
    context = {'user_form': user_form}
    return render(request, 'accounts/update.html', context)

@login_required
def password(request):
    if request.method == 'POST':
        user_form = PasswordChangeForm(request.user, request.POST) # 순서 주의!
        if user_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            return redirect('boards:index')
    else:
        user_form = PasswordChangeForm(request.user) # instance= 아님 주의!
    context = {'user_form': user_form}
    return render(request, 'accounts/update.html', context)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    