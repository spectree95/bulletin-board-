import json
from main.models import Product
from .models import Message,Room
from datetime import datetime, timezone
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope['user']
        if hasattr(self.user, "_wrapped") and self.user._wrapped is not None:
            self.user = self.user._wrapped 
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.personal_group = f"user_chats_{self.user.id}"
        await self.channel_layer.group_add(self.personal_group, self.channel_name)
        
        
        self.product_id = self.scope["url_route"]["kwargs"].get('pk')
        if self.product_id:
            product,img = await self.get_product_data(self.product_id)
            self.product = product
            self.product_img = img
            room, created = await self.get_or_create_room(product, product.author, self.user)
            self.group_name = f"chat_product{room.id}"

            await self.channel_layer.group_add(self.group_name, self.channel_name)


        await self.accept()


    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        command = data.get("command", None)
        if command == "join":
            self.room_id = data.get("room_id")
            
            await self.join_room(self.room_id)
            
        elif command == "send":
            message = data.get("message", "").strip()
            room_id = data.get("room_id")
            if not message or not room_id:
                return

            info = await self.save_message(room_id, message)
            if info is None:
                return

            created = datetime.now(timezone.utc).isoformat()

            await self.channel_layer.group_send(f"chat_product{room_id}", {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "room_id": room_id,
                "sender_name": self.user.username,
                "created": created,
            })

            await self.channel_layer.group_send(f"user_chats_{info['recipient_id']}", {
                "type": "new_message_for_user",
                "room_id": room_id,
                "sender_name": self.user.username,
                "last_message": message,
                "product_id": info["product_id"],
                "product_img": info["product_img"],
            })    
            
    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name,self.channel_name)
            
        if hasattr(self, "personal_group"):
            await self.channel_layer.group_discard(self.personal_group, self.channel_name)
    
    
    async def chat_message(self,event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
            "room_id": event["room_id"],
            "created": event["created"]
        }))
            
    
    async def new_message_for_user(self,event):
        await self.send(text_data=json.dumps({
            "type": "new_message_for_user",
            "room_id": event["room_id"],
            "sender_name": event["sender_name"],
            "last_message": event["last_message"],
            "product_id": event["product_id"],
            "product_img": event["product_img"],
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
                "created": msg["created"].isoformat()
            }))
        
        
    @database_sync_to_async
    def get_product_data(self,product_id):
        product = Product.objects.select_related("author").get(id=product_id)        
        first_img = product.images.first()
        img = first_img.image.url if first_img else "/static/images/default.jpg"
        return product,img

 
    @database_sync_to_async    
    def get_or_create_room(self,product,user_a,user_b):
        if not hasattr(user_a, "id") and not hasattr(user_b, 'id'):
            raise ValueError("user_a или user_b не пользователь!")
        return Room.objects.get_or_create(
            product = product,
            user_a = user_a,
            user_b = user_b
        )
        
    @database_sync_to_async
    def save_message(self, room_id, text):
        try:
            room = Room.objects.select_related("product").get(id=room_id)
        except Room.DoesNotExist:
            return None
        if self.user.id not in (room.user_a_id, room.user_b_id):
            return None

        Message.objects.create(room=room, sender=self.user, text=text)

        recipient_id = room.user_a_id if room.user_b_id == self.user.id else room.user_b_id
        first_img = room.product.images.first()
        return {
            "recipient_id": recipient_id,
            "product_id": room.product_id,
            "product_img": first_img.image.url if first_img else "/static/images/default.jpg",
        }