from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Board
from .forms import BoardForm
import pprint, hashlib
from django.views.decorators.http import require_http_methods
# Create your views here.

def index(request):
    pprint.pprint(request.user.is_superuser)
    boards = Board.objects.order_by('-pk')
    if request.user.is_authenticated:
        gravatar_url = hashlib.md5(request.user.email.strip().lower().encode('utf-8')).hexdigest()
    else:
        gravatar_url = None
    # d0e53a9a9bbc9cf481144a929930f41c
    context = {'boards': boards, 'gravatar_url': gravatar_url}
    return render(request, 'boards/index.html', context)

@login_required    
def create(request):
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            # board = Board()
            # board.title = board_form.cleaned_data.get('title')
            # board.content = board_form.cleaned_data.get('content')
            # board.user = request.user
            # board.save()
            
            board = board_form.save(commit=False) # 돈을 보냈을 때 돈이 아직 들어오기전에는 틀만만들어두고 save하지 않는것
            board.user = request.user # 추가 작업을 해주고, 즉 commit=False 는 추가작업을 해주기 위한 것.
            board.save() # save를 해준다. 
            return redirect(board)
    else:
        board_form = BoardForm()
    context = {'board_form': board_form}
    return render(request, 'boards/form.html', context)

def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    board.hit += 1
    board.save()
    context = {'board': board}
    return render(request, 'boards/detail.html', context)
  
# @require_http_methods(["POST"])
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # board = Board.objects.get(pk=board_pk)
    if request.method == "POST":
        board.delete()
        return redirect('boards:index')
    else:
        if request.user != board.user:
            return redirect(board)
        return redirect(board)
        
# @require_http_methods(["POST"])
def edit(request, board_pk):
    # 1. board_pk에 해당하는 오브젝트르 가져온다.
    #    만약에 없으면 404 에러
    #    만약에 있으면 board = Board.objects.get(pk=board_pk)와 동일.
    board = get_object_or_404(Board, pk=board_pk)
    # 2-1. POST 요청이면 (사용자가 form을 통해 데이터를 보내준 것.)
    if request.method == "POST":
        
        # 사용자 입력값(request.POST)을 BoardForm에 전달해주고, 
        board_form = BoardForm(request.POST, instance=board)
        
        # 검증 (유효성 체크)
        if board_form.is_valid():
            # board.title = board_form.cleaned_data.get('title')
            # board.content = board_form.cleaned_data.get('content')
            # board.save()
            board = board_form.save()
            return redirect(board)
    # 2-2: GET 요청이면 (수정하기 버튼을 눌렀을 때)
    else:
        # if request.user != board.user:
            # return redirect(board)
        # BoardForm을 초기화(사용자 입력값을 넣어준 상태)
        # board_form = BoardForm(initial=board.__dict__) 이렇게 작성해도 가능
        board_form = BoardForm(instance=board)
    # context에 담겨 있는 board_form은 아래와 같이 가능함.
    # 1 - POST 요청에서 검증에 실패하였을 때, 오류 메시지가 포함된 상태
    # 2 - GET 요청에서 초기화된 상태
    context = {'board_form': board_form}
    return render(request, 'boards/form.html', context)
    