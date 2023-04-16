from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('class9', views.class9, name='class9'),
    path('class10', views.class10, name='class10'),
    path('class11', views.class11, name='class11'),
    path('register', views.register, name='register'),

    path('home_video/stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('home_video/<int:pk>/', views.get_video, name='video'),
    path('home_video', views.get_list_video, name='home_video')

]
