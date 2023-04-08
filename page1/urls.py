from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('class9', views.class9, name='class9'),
    path('class10', views.class10, name='class10'),
    path('class11', views.class11, name='class11')

]