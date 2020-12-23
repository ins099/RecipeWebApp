from django.contrib import admin
from . models import Category, Recipe, Following,Comment
# Register your models here.

admin.site.register(Category)
admin.site.register(Following)
admin.site.register(Recipe)
admin.site.register(Comment)

