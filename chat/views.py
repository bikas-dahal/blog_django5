from django.shortcuts import render, redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from django.db.models import Q 


# Create your views here.

class Main(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect('home')
        
        data = {
            'type': 'receiver_function',
            'message': 'n hy views'
        }
        
        channel_layer = get_channel_layer() 
        
        async_to_sync(channel_layer.group_send)('group_channel', data)
        
        
        print(request.session.get('from_consumer'))
        request.session['get_me_from_consumer'] = 'hyalo'
        return render(request, 'chat/main.html') 
    
    
class Login(View):
    def get(self, request):
        return render(request, 'chat/login.html') 
    
    def post(self, request):
        context = {}
        
        data = request.POST.dict()
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(
            request=request,
            username = username,
            password = password
        )
        if user != None:
            login(request, user)
            return redirect('home')
            
        context = {
            'error': 'Invalid Credentials'
        }
        return render (request, 'chat/login.html', context)

        
class Register(View):
    def get(self, request):
        return render(request, 'chat/register.html') 
    
    def post(self, request):
        
        context = {}
        
        
        data = request.POST.dict()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        try:
            new_user = User() 
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
            
            user = authenticate(
                request=request,
                username = username,
                password = password
            )
            
            if user != None:
                login(request, user)
                return redirect('home') 
        except:
            context['error'] = 'Username or Email already exists'
            
        return render(request, 'chat/register.html', context)
            
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main')
    
     
class Home(View):
    def get(self, request):
        print(request.session.items())
        
        if request.user.is_authenticated:
            users = User.objects.all()
            
            context = {
                'user': request.user,
                'users': users
            }
            return render(request, 'chat/home.html', context) 
        
        return redirect('main')
    
class ChatPerson(View):
    def get(self, request, id):
        
        person = User.objects.get(id = id)
        me = request.user
        
        messages = models.Message.objects.filter(Q(sender = me, receiver = person) | Q(sender = person, receiver = me)).order_by('date', 'time')

        # user_channel_name = models.UserChannel.objects.get(user = person)

        # data = {
        #             'type': 'receiver_function',
        #             'type_of_data': 'seen',
        #         }
                
        # channel_layer = get_channel_layer()
        
        
        # async_to_sync(channel_layer.send)(user_channel_name.channel_name, data)

        # seen = models.Message.objects.filter(sender = person, receiver= me)
        # seen.update(seen = True)
        
        context = {
            'person': person,
            'me': me,
            "messages" : messages
        }
                
        return render(request, 'chat/chat_person.html', context) 
    
    