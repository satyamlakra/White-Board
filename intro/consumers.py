from functools import reduce
import json

from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.db.models import Q
import operator
# from django_q.tasks import async_task
from asgiref.sync import async_to_sync
from intro.models import MyUser,boardobject

from urllib import request

class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            print(self.scope)
        
        
            # ruser  = MyUser.objects.filter(email=self.room_name).first()
            # self.room_group_name = "sc_%s" % ruser.mobile_number
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "sc_%s" % self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            print(self.room_name)
            await self.accept()
        
           
           
        
        
    async def disconnect(self, close_code):
       
            try: 
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            except:
                 print('worng_entry')
                 self.connected = False   
         
       
        
       

    async def receive(self, text_data):
       
        text_data_json =  text_data
        message = text_data_json
        
             
        
        if message!="":
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": message}
                                            )
        # if  data!="":

    async def live_message(self, event,type='live_message'):
        
     
        message = event['message']

        await self.send(text_data=message)
    

class NewConsumerchat(AsyncWebsocketConsumer):
    async def connect(self):
       
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            print(self.scope)
        
        
            # ruser  = MyUser.objects.filter(email=self.room_name).first()
            # self.room_group_name = "sc_%s" % ruser.mobile_number
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "rc_%s" % self.room_name
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            print(self.room_name)
            await self.accept()
        
           
           
        
        
    async def disconnect(self, close_code):
       
            try: 
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            except:
                 print('worng_entry')
                 self.connected = False   
         
       
        
       

    async def receive(self, text_data):
       
        text_data_json =  text_data
        message = text_data_json
        
             
        
        if message!="":
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": message}
                                            )
        # if  data!="":

    async def live_message(self, event,type='live_message'):
        boardobject.objects.get()
     
        message = event['message']

        await self.send(text_data=message)
    

    
    