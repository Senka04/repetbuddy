from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('class10', views.class10, name='class10')
]