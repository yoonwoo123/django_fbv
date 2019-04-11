from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('<int:board_pk>/', views.detail, name="detail"),
    path('<int:board_pk>/delete/', views.delete, name="delete"),
    path('<int:board_pk>/edit/', views.edit, name="edit"),
    path('<int:board_pk>/userdetail/', views.userdetail, name="userdetail"),
]