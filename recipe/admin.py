from django.contrib import admin
from . models import Category, Recipe, Following,Comment, User
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Following)
admin.site.register(Recipe)
admin.site.register(Comment)

