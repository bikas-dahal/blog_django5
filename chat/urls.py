from django.urls import path 
from . import views

urlpatterns = [
    path('chat/', views.Main.as_view(), name='main'),
    path('chat/login ', views.Login.as_view(), name='login'),
    path('chat/register', views.Register.as_view(), name='register'),
    path('chat/logout', views.Logout.as_view(), name='logout'),
    path('chat/home', views.Home.as_view(), name='home'),
    path('chat/chat_person/<int:id>', views.ChatPerson.as_view(), name='chat_person'),
    
]

