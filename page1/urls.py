from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home', views.gohome, name='home'),
    path('', views.hello_page, name='hello_page'),
    path('search', views.search, name='search'),
    path('home_user', views.user_main, name='home_user'),
    path('home_tutor', views.tutor_main, name='home_tutor'),
    path('login', views.login_view, name='login'),
    path('confirm_logout', views.confirm_logout, name='confirm_logout'),
    path('logout', views.logout_view, name='logout'),
    path('courses', views.courses, name='courses'),
    path('course_create', views.course_create, name='course_create'),
    path('course_create_post', views.course_create_post, name='course_create_post'),
    path('register', views.register, name='register'),
    path('home_video/stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('home_video/<int:pk>/', views.get_video, name='video'),
    path('home_video', views.get_list_video, name='home_video'),
    path('upload_video', views.upload_video, name='upload_video'),
    path('home_video/<int:pk>/delete/', views.delete_video, name='delete_video'),
    path('home_video/<int:pk>/confirm_delete/', views.confirm_delete_video, name='confirm_delete_video'),
]
