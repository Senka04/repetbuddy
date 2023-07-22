from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
import uuid
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubSubcategory(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    uuid = models.UUIDField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.uuid:
            timestamp = timezone.now().timestamp()
            data = f"{self.pk}{timestamp}"
            self.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, data)
        super().save(*args, **kwargs)

    name = models.CharField(max_length=26)
    content = CKEditor5Field(verbose_name='Текст курса', config_name='extends', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    image = models.ImageField(upload_to='uploads/previews/', null=True, blank=True)
    file = models.FileField(
        upload_to='uploads/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=30, null=True)
    # Добавьте другие поля для профиля пользователя

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=30, null=True)
    discipline = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def is_tutor(self):
        return True

    def __str__(self):
        return f'{self.user.username}'


class Video(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/previews/')
    file = models.FileField(
        upload_to='uploads/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
