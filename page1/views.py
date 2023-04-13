from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Video
from .services import open_file

def index(request):
    return render(request, 'page1/index.html') # представляем, что мы уже в templates
def registration(request):
    return render(request, 'page1/registration.html') # представляем, что мы уже в templates
def login(request):
    return render(request, 'page1/login.html') # представляем, что мы уже в templates
def class9(request):
    return render(request, 'page1/class9.html')
def class10(request):
    return render(request, 'page1/class10.html')
def class11(request):
    return render(request, 'page1/class11.html')
# Create your views here.
def get_list_video(request):
    return render(request, 'page1/home.html', {'video_list': Video.objects.all()})


def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    return render(request, "page1/video.html", {"video": _video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response