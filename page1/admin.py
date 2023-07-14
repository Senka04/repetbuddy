from django.contrib import admin
from .models import Video, Course, Category, Subcategory, SubSubcategory

admin.site.register(Video)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(SubSubcategory)
# Register your models here.
