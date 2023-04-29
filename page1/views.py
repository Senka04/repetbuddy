from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, User
from .services import open_file
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import VideoForm


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



@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Видео успешно загружено.')
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'page1/videopleer/upload_video.html', {'form': form})

@login_required
def confirm_delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'page1/videopleer/confirm_delete_video.html', {'video': video})
@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.user != video.user:
        messages.error(request, "You don't have permission to delete this video.")
        return redirect('home')
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video has been deleted successfully!')
        return redirect('home')
    return render(request, 'delete_video.html', {'video': video})

@login_required
def get_list_video(request):
    video_list = Video.objects.filter(user=request.user)
    return render(request, 'page1/videopleer/home.html', {'video_list': video_list})


@login_required
def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk, user=request.user)
    return render(request, "page1/videopleer/video.html", {"video": _video})

@login_required
def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)

    # Check if the video belongs to the user
    video = get_object_or_404(Video, id=pk, user=request.user)

    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response