from django.contrib import admin
from django.urls import path
from intro import views
from django.views.generic.base import TemplateView
urlpatterns = [
    
    path('',views.login,name='login'),
    path('indexapi/',views.indexapi,name='api'),
    path('index/',views.meet,name='index'),
    path('postmeet/',views.postmeet,name='postmeet'),
    path('remove/',views.remove,name='remove'),
    path('signup/',views.build,name='loginProfie'),
   
    path('logout/',views.logout,name='logout'),
    path('api/current_user/', views.current_user, name='current_user'),
   
    
    
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
 
    path("password_reset/", views.password_reset_request, name="password_reset")
]
