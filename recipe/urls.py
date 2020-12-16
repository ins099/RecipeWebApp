from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('allrecipes', views.allrecipes, name = 'allrecipes'),
    path('create', views.createrecipe, name='create')
]