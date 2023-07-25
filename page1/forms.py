from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Video, TutorProfile, UserProfile, Course


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'content', 'image', 'file', 'description')
        labels = {
            'name': 'Название',
            'content': 'Курс',
            'image': 'Обложка',
            'file': 'Видео',
            'description': 'Краткое описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class CourseUpdateForm(CourseCreateForm):
    class Meta:
        model = Course
        fields = CourseCreateForm.Meta.fields
        labels = {
            'name': 'Название',
            'content': 'Курс',
            'image': 'Обложка',
            'file': 'Видео',
            'description': 'Краткое описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg btn-primary'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg btn-primary'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'file': 'Видео',
            'image': 'Обложка',
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True)
    is_tutor = forms.BooleanField(required=False)
    discipline = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_tutor', 'discipline']

    def clean(self):
        cleaned_data = super().clean()
        self.errors.clear()

        username = cleaned_data.get('username')
        if not username:
            self.add_error('username', 'Пожалуйста, введите никнейм.')
        elif UserProfile.objects.filter(username=username).exists() or TutorProfile.objects.filter(
                username=username).exists():
            self.add_error('username', 'Пользователь с таким никнеймом уже существует.')

        email = cleaned_data.get('email')
        if not email:
            self.add_error('email', 'Пожалуйста, введите электронную почту.')
        elif UserProfile.objects.filter(email=email.lower()).exists() or TutorProfile.objects.filter(email=email.lower()).exists():
            self.add_error('email', 'Эта электронная почта уже используется.')

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1:
            self.add_error('password1', 'Пожалуйста, введите пароль.')
        elif len(password1) < 8:
            self.add_error('password1', 'Пароль должен содержать как минимум 8 символов')
            self.errors.pop('password2', None)
        if password1 is not None and (password1.isdigit() or password1.isalpha()):
            self.add_error('password1', 'Пароль должен содержать как минимум одну букву и одну цифру.')
            self.errors.pop('password2', None)
        if not password2:
            self.add_error('password2', 'Пароли не совпадают.')

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if self.cleaned_data['is_tutor']:
            tutor_profile = TutorProfile.objects.create(
                user=user,
                discipline=self.cleaned_data['discipline'].lower(),
                email=self.cleaned_data['email'].lower(),
                username=self.cleaned_data['username'],
            )
            tutor_profile.save()
        else:
            user_profile = UserProfile.objects.create(
                user=user,
                email=self.cleaned_data['email'].lower(),
                username=self.cleaned_data['username']
            )
            user_profile.save()

        if commit:
            user.save()

        return user



