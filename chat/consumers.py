from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json 
from . import models
from django.contrib.auth.models import User
import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope)
        print(self.scope.get('user'))
        
        
        
        try:
            user_channel = models.UserChannel.objects.get(user = self.scope.get('user'))
            user_channel.channel_name = self.channel_name 
            user_channel.save()
            
        except:
            user_channel = models.UserChannel()
            user_channel.user = self.scope.get("user")
            user_channel.channel_name = self.channel_name 
            user_channel.save()
        
        self.person_id = (self.scope.get('url_route').get('kwargs').get('id'))
        



    def receive(self, text_data):
        # print(dir(self.scope))
        
        receiver = User.objects.get(id = self.person_id)
        
        now = datetime.datetime.now()
        date = now.date() 
        time = now.time()
        
        text_data = json.loads(text_data)
        
        if text_data.get('type') == 'new_message':
            print(text_data.get("type"))
            print(text_data.get("message"))
            print(self.scope['user'])
            
            new_message = models.Message() 
            new_message.sender = self.scope['user'].username
            new_message.receiver = receiver
            new_message.message = text_data.get("message")
            new_message.date = date
            new_message.time = time 
            new_message.seen = False
            new_message.save()
            
            try:
                receiver_channel_name = models.UserChannel.objects.get(user = receiver)
            
                data = {
                    'type': 'receiver_function',
                    'type_of_data': 'new_message',
                    'data': text_data.get("message")
                }
                
                async_to_sync(self.channel_layer.send)(receiver_channel_name.channel_name, data)
            
            except:
                pass 
            
        elif text_data.get('type') == 'i_have_seen':
            try:
                receiver_channel_name = models.UserChannel.objects.get(user = receiver)
            
                data = {
                    'type': 'receiver_function',
                    'type_of_data': 'seen',
                }
                
                async_to_sync(self.channel_layer.send)(receiver_channel_name.channel_name, data)

                seen = models.Message.objects.filter(sender = self.scope.get("user"), receiver= receiver)
                seen.update(seen = True)
            except:
                pass 
        

        
    
    def receiver_function(self, data_from_layer):
        print(data_from_layer)
        
        data = json.dumps(data_from_layer)
        self.send(data)
