from django.db import models
from main.models import Product 
from bulletin_board import settings

# Create your models here.

class Room(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rooms")
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rooms_a")
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rooms_b")
    latest_messages = models.ForeignKey("Message", on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    
    @property
    def last_message(self):
        return self.messages.order_by("-created").first()
    
    class Meta:
        constraints = [ 
            models.UniqueConstraint(fields=['product', 'user_a', 'user_b'], name="unique_name_pair")
        ]
    
class Message(models.Model):
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"[{self.room}] {self.sender}: {self.text[:30]}"
    
    
    