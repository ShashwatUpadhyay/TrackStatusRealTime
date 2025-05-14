from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . import models
        
class OrderProgress(WebsocketConsumer):
    def connect(self, **kwargs):
       self.room_name = self.scope['url_route']['kwargs']['order_id']
       self.room_group_name = f'order_{self.room_name}'
       async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )         
       order = models.Order.give_order_detail(self.room_name) 
       self.accept()
       self.send(text_data=json.dumps({
           "payload": order
       }))        
       
    def order_status(self, event):
        data = json.loads(event['value'])
        self.send(text_data=json.dumps({
            "payload": data
        }))
   
            
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
    
    def disconnect(self, code):
        pass
    