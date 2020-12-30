from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('api/allrecipes', views.allrecipes, name = 'allrecipes'),
    path('create', views.createrecipe, name='create'),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('recipe/<int:id>', views.RecipeView, name = 'recipeid'),
    path('profile/<str:username>', views.userProfile, name = 'profile'),
    path('follow', views.Follow, name='follow'),
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike'),
    path('comment', views.CommentSubmit, name = 'comment'),
    path('category', views.ListCategory, name = 'category'),
    path('AllRecipe', views.AllRecipes, name = 'AllRecipe'),
]