from django.urls import path
from . import views

urlpatterns = [
    path('areas/<area>', views.areas, name="areas"),
    path('polls/<int:poll_id>', views.polls, name="polls"),
    path('areas/<area>/result', views.result, name="result"),
    path('pollhome/', views.poll_home, name="poll_home"),
    path('add/', views.add, name="add"),
    path('create/', views.create, name="create"),
]