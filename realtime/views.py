from django.shortcuts import render
from django.views.generic import DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Product
from .models import Room, Message
from django.db.models import Q


class Chat_author(DetailView):
    model = Product
    template_name = "realtime/chat_author.html"
    context_object_name = "product"
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object 
        author = product.author
        room, created = Room.objects.get_or_create(
            product=product,
            user_a = author,
            user_b = self.request.user
            )
        print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {created}")
        print(f"{room}")
        
        context["messages"] = Message.objects.filter(room=room)
        return context
class Messenger(ListView):
    model = Room
    template_name = "realtime/Messenger.html"
    context_object_name = "rooms"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(user_a = self.request.user) | Q(user_b = self.request.user)
        ).distinct().order_by("latest_messages__created")
        return queryset
    