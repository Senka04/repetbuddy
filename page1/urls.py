from django.urls import path, include
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
    path('my_courses', views.courses, name='courses'),
    path('course_create', views.course_create, name='course_create'),
    path('course_create_post', views.course_create_post, name='course_create_post'),
    path('course_update/<str:pk>/', views.course_update, name='course_update'),
    path('course_update_post/<str:pk>/', views.course_update_post, name='course_update_post'),
    path('register', views.register, name='register'),
    path('tutor_info/<int:user_id>/', views.tutor_info, name='tutor_info'),
    path('course_read/<str:pk>/', views.course_read, name='course_read'),
    path('home_video/stream/<str:pk>/', views.get_streaming_video, name='stream'),
    path('home_video/<str:pk>/', views.get_video, name='video'),
    path('home_video', views.get_list_video, name='home_video'),
    path('upload_video', views.upload_video, name='upload_video'),
    path('home_video/<int:pk>/delete/', views.delete_video, name='delete_video'),
    path('home_video/<int:pk>/confirm_delete/', views.confirm_delete_video, name='confirm_delete_video'),
    path('course_update/<str:pk>/delete/', views.delete_course, name='delete_course'),
    path('courses/<str:pk>/', views.from_filter, name='from_filter'),
]
