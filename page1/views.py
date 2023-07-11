import uuid
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, TutorProfile, Course, UserProfile
from .services import open_file
from .forms import RegistrationForm, CourseCreateForm, CourseUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import VideoForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def course_read(request, pk: str):
    # Получаем отформатированный текст из базы данных
    course = Course.objects.get(uuid=pk)
    content = course.content
    return render(request, 'page1/course_read.html', {'content': content})


def tutor_info(request, user_id: int):
    tutor = TutorProfile.objects.get(user_id=user_id)
    video_list = Video.objects.filter(user_id=user_id)
    course_list = Course.objects.filter(author=user_id)
    return render(request, 'page1/tutor_info.html', {'tutor': tutor, 'video_list': video_list, 'course_list': course_list})


@login_required
def confirm_logout(request):
    return render(request, 'page1/registration/confirm_logout.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('hello_page')
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
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'page1/registration/register.html', {'form': form})
@login_required
def tutor_main(request):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            return render(request, 'page1/tutor_main.html')  # представляем, что мы уже в templates
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def user_main(request):
    try:
        user_profile = UserProfile.objects.get(username=request.user)
        if user_profile:
            return render(request, 'page1/user_main.html')  # представляем, что мы уже в templates
    except UserProfile.DoesNotExist:
        return redirect('home_tutor')


def hello_page(request):
    cards = Course.objects.filter()
    return render(request, 'page1/hello_page.html', {'cards': cards})


def search(request):
    search_info = request.GET.get('search_info')
    if search_info:
        vector = SearchVector('name', 'description')
        query = SearchQuery(search_info)
        rank = SearchRank(vector, query)
        obj = Course.objects.annotate(rank=rank, search=vector).filter(search=query).order_by('-rank')
    else:
        obj = Course.objects.none()
    params = {'obj': obj}
    return render(request, 'page1/search.html', params)


def gohome(request):
    if not request.user.is_authenticated:
        return redirect('hello_page')
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            return redirect('home_tutor')
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def courses(request):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            course_list = Course.objects.filter(author=request.user)
            return render(request, 'page1/courses.html', {'course_list': course_list})
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def course_create(request):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            form = CourseCreateForm()
            return render(request, 'page1/course_create.html', {'form': form})
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def course_create_post(request):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            if request.method == 'POST':
                form = CourseCreateForm(request.POST, request.FILES)
                if form.is_valid():
                    course = form.save(commit=False)
                    course.author = request.user
                    course.uuid = uuid.uuid4()
                    course.save()
                    return redirect('courses')
                else:
                    print("Form is not valid")  # Отладочное сообщение
                    print("Errors:", form.errors)  # Отладочное сообщение
            else:
                form = CourseCreateForm()

            return render(request, 'page1/course_create.html', {'form': form})
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def course_update(request, pk: str):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            course = get_object_or_404(Course, uuid=pk, author=request.user)
            form = CourseUpdateForm(instance=course)
            return render(request, 'page1/course_update.html', {'form': form, 'course': course})
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def course_update_post(request, pk: str):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            course = get_object_or_404(Course, uuid=pk, author=request.user)
            if request.method == 'POST':
                form = CourseUpdateForm(request.POST, request.FILES, instance=course)
                if form.is_valid():
                    form.save()
                    return redirect('courses')
            else:
                form = CourseUpdateForm(instance=course)
            return render(request, 'page1/course_update.html', {'form': form, 'course': course})
    except TutorProfile.DoesNotExist:
        return redirect('home_user')



@login_required
def delete_course(request, pk: str):
    try:
        tutor_profile = TutorProfile.objects.get(username=request.user)
        if tutor_profile:
            course = get_object_or_404(Course, uuid=pk, author=request.user)
            course.delete()
            return redirect('courses')
    except TutorProfile.DoesNotExist:
        return redirect('home_user')


@login_required
def upload_video(request):
    try:
        tutor_profile = TutorProfile.objects.get(user=request.user)
    except TutorProfile.DoesNotExist:
        return redirect('home_user')
    if tutor_profile:
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video = form.save(commit=False)
                video.user = request.user
                video.uuid = uuid.uuid4()
                video.save()
                messages.success(request, 'Видео успешно загружено.')
                return redirect('home_tutor')
        else:
            form = VideoForm()
        return render(request, 'page1/videopleer/upload_video.html', {'form': form})


@login_required
def confirm_delete_video(request, pk):
    try:
        tutor_profile = TutorProfile.objects.get(user=request.user)
    except TutorProfile.DoesNotExist:
        return redirect('home_user')
    if tutor_profile:
        video = get_object_or_404(Video, pk=pk)
        if request.user == video.user:
            return render(request, 'page1/videopleer/confirm_delete_video.html', {'video': video})


@login_required
def delete_video(request, pk):
    try:
        tutor_profile = TutorProfile.objects.get(user=request.user)
    except TutorProfile.DoesNotExist:
        return redirect('home_user')
    if tutor_profile:
        video = get_object_or_404(Video, pk=pk)
        if request.user != video.user:
            messages.error(request, "You don't have permission to delete this video.")
            return redirect('home_user')
        if request.method == 'POST':
            video.delete()
            messages.success(request, 'Video has been deleted successfully!')
            return redirect('home_tutor')



def get_list_video(request):
    video_list = Video.objects.filter(user=request.user)
    return render(request, 'page1/videopleer/home.html', {'video_list': video_list})



def get_video(request, pk: str):
    _video = get_object_or_404(Video, uuid=pk)
    return render(request, "page1/videopleer/video.html", {"video": _video})



def get_streaming_video(request, pk: str):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
