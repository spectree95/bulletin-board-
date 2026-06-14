from django.urls import re_path,path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat_author/(?P<pk>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/Messenger/$", ChatConsumer.as_asgi()),
]   