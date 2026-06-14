import json
from main.models import Product
from .models import Message,Room
from bulletin_board import settings
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope['user']
        if hasattr(self.user, "_wrapped") and self.user._wrapped is not None:
            self.user = self.user._wrapped 
        product_id = self.scope["url_route"]["kwargs"].get('pk')
        if product_id:
            product = await self.get_product(product_id)
            author = product.author
            room, created = await self.get_or_create_room(product, author, self.user)
            self.group_name = f"chat_product_{room.id}"
            self.room = room
            await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()


    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        command = data.get("command", None)
        if command == "join":
            self.room_id = data.get("room_id")
            
            await self.join_room(self.room_id)
            
        elif command == "send":
            message = data.get("message", "")
            room_id = data.get("room_id")
            if room_id:
                self.room = await database_sync_to_async(Room.objects.get)(id=room_id)
            
            await database_sync_to_async(Message.objects.create)(
                room = self.room,
                sender = self.user,
                text = message
            )
            
            await self.channel_layer.group_send(self.group_name,{
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "room_id": self.room.id,
                "sender_name": self.user.username
                
            })
            
    
    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name,self.channel_name)
    
    async def chat_message(self,event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
            "room_id": event["room_id"],
        }))
            
            
    async def join_room(self, room_id):
        if getattr(self, "group_name", None):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)    
        
        room = await database_sync_to_async(Room.objects.get)(id=room_id)
        self.group_name = f"chat_product{room.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        messages = await database_sync_to_async(list)(
            Message.objects.filter(room=room)
        .order_by("created")
        .values("sender__username", "text", "created"))
        
        
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg["text"],
                "sender_name": msg["sender__username"],
                "created": str(msg["created"])
            }))
        
        
    @database_sync_to_async
    def get_product(self,product_id):
        return Product.objects.select_related("author").get(id=product_id)        
    


 
    @database_sync_to_async    
    def get_or_create_room(self,product,user_a,user_b):
        if not hasattr(user_a, "id") and not hasattr(user_b, 'id'):
            raise ValueError("user_a или user_b не пользователь!")
        return Room.objects.get_or_create(
            product = product,
            user_a = user_a,
            user_b = user_b
        )