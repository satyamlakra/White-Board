from django.urls import re_path

from intro import consumers

#r"ws/sc/(?P<room_name>\w+)/$"
websocket_urlpatterns = [
    re_path(r"ws/sc/sc/(?P<room_name>\w+)/$", consumers.NewConsumer.as_asgi()),
    re_path(r"ws/rc/rc/(?P<room_name>\w+)/$", consumers.NewConsumerchat.as_asgi()),
   
]