
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.signout, name="signout"),
    path('addtodo/', views.addtodo, name="addtodo"),
    path('deletetodo/<int:pk>/', views.delete_todo, name="delete_todo"),
    path('updatetodo/<int:pk>/<str:status>/', views.updatetodo, name="updatetodo"),
]
