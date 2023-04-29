from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Video, TutorProfile
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    is_tutor = forms.BooleanField(required=False)
    discipline = forms.CharField(max_length=50, required=False)
    hourly_rate = forms.DecimalField(max_digits=6, decimal_places=2, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_tutor', 'discipline', 'hourly_rate']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()

        if self.cleaned_data['is_tutor']:
            tutor_profile = TutorProfile(user=user, discipline=self.cleaned_data['discipline'],
                                         hourly_rate=self.cleaned_data['hourly_rate'])
            tutor_profile.save()

        return user


