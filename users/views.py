from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

def index(request):
    User = get_user_model()
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users/index.html', context)

def detail(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    # board 는 유저를 1개만 갖고 있으므로 boards.user 이고 user는 여러개의 board를 갖고있으므로
    boards = user.board_set.all()
    context = {'user_detail': user, 'boards': boards}
    return render(request, 'users/detail.html', context)
