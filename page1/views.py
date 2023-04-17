from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
from .services import open_file
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse

@login_required
def confirm_logout(request):
    return render(request, 'page1/registration/confirm_logout.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect(reverse('confirm_logout'))
def login_view(request):
    # Проверяем, был ли уже выполнен вход на сайт
    if request.user.is_authenticated:
        return redirect('home')

    # Если это POST-запрос, обрабатываем данные формы
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Если форма валидна, выполняем вход на сайт
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    # Отображаем страницу с формой входа на сайт
    return render(request, 'page1/registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'page1/registration/register.html', {'form': form})

def index(request):
    return render(request, 'page1/index.html') # представляем, что мы уже в templates

def class9(request):
    return render(request, 'page1/class9.html')
def class10(request):
    return render(request, 'page1/class10.html')
def class11(request):
    return render(request, 'page1/class11.html')
# Create your views here.
def get_list_video(request):
    return render(request, 'page1/videopleer/home.html', {'video_list': Video.objects.all()})


def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    return render(request, "page1/videopleer/video.html", {"video": _video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response