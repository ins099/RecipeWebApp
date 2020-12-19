from django.contrib import admin
from . models import Category, Recipe, Following
# Register your models here.

admin.site.register(Category)
admin.site.register(Following)
admin.site.register(Recipe)
