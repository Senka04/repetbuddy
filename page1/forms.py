from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Video, TutorProfile, UserProfile


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
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    patronymic = forms.CharField(max_length=30)
    is_tutor = forms.BooleanField(required=False)
    discipline = forms.CharField(max_length=50, required=False)
    hourly_rate = forms.DecimalField(max_digits=6, decimal_places=2, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'is_tutor',
                  'discipline', 'hourly_rate']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("Необходимо указать пароль.")
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2
    def save(self, commit=True):
        user = super().save(commit=True)
        if self.cleaned_data['is_tutor']:
            tutor_profile = TutorProfile.objects.create(
                user=user,
                discipline=self.cleaned_data['discipline'].lower(),
                hourly_rate=self.cleaned_data['hourly_rate'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                patronymic=self.cleaned_data['patronymic'],
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username']
            )
            tutor_profile.save()
        else:
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                patronymic=self.cleaned_data['patronymic'],
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username']
            )
            user_profile.save()

        if commit:
            user.save()

        return user
