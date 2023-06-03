from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Course(models.Model):
    name = models.CharField(max_length=100)
    content = CKEditor5Field(verbose_name='Текст курса', config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f'{self.name}'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    patronymic = models.CharField(max_length=30, null=True)
    # Добавьте другие поля для профиля пользователя

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    patronymic = models.CharField(max_length=30, null=True)
    discipline = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def is_tutor(self):
        return True

    def __str__(self):
        return f'{self.user.username}'

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='image/')
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
