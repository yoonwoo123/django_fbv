import pprint
from django.shortcuts import render, redirect
# from .forms import UserForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import UserCustomChangeForm
# Create your views here.
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:
        user_form = UserCreationForm()
    context = {'user_form': user_form}
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
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
@require_http_methods(["POST"]) # 삭제는 GET요청을 아예 받지 않기 때문에 POST만 해줘도 상관없다.
def delete(request):
    # if request.method == 'POST':
    # 유저 오브젝트를 가져와서 삭제한다.
    request.user.delete()
    return redirect('boards:index')
    
# @login_required
# def delete(request):
#     if request.method == 'POST':
#     request.user.delete()
#     return redirect('boards:index')

@require_http_methods(["GET", "POST"]) # GET과 POST를 두개만 받으면서 if else로 걸러준다. 
def update(request):
    # user_form = UserChangeForm()
    if request.method == 'POST':

        user_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_form.is_valid(): # 만약에 유저 폼이 유효하다면 유저폼을 저장하고
            user_form.save()
            return redirect('boards:index')
    else:
        user_form = UserCustomChangeForm(instance=request.user)
    context = {'user_form': user_form}
    return render(request, 'accounts/update.html', context)
    
@login_required
def password(request):
    if request.method == 'POST':
        user_form = PasswordChangeForm(request.user, request.POST) # 순서 주의 !
        if user_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            return redirect('boards:index')
    else:
        user_form = PasswordChangeForm(request.user) # instance= 아님 주의
    context = {'user_form': user_form}
    return render(request, 'accounts/update.html', context)