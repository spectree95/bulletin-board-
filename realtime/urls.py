from django.urls import path 
from .views import Chat_author,Messenger

app_name = "realtime"

urlpatterns = [
    path("chat_author/<int:pk>/", Chat_author.as_view(), name="chat_author"),
    path("Messenger", Messenger.as_view(), name="Messenger"),
    
]
