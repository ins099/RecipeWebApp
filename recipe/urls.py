from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('mostliked', views.MostLikeRecipeView.as_view(), name = 'mostliked'),
    path('recentrecipes', views.RecentRecipeView.as_view(), name = 'recentrecipes'),
    path('create', views.createrecipe, name='create'),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('recipe/<int:id>', views.RecipeView, name = 'recipeid'),
    path('profile/<str:username>', views.userProfile, name = 'profile'),
    path('follow', views.Follow, name='follow'),
    path('like', views.like, name='like'),
    path('comment', views.CommentSubmit, name = 'comment'),
    path('category', views.ListCategory, name = 'category'),
    path('AllRecipe', views.AllRecipes, name = 'AllRecipe'),
    path('search', views.search, name='search'),
    path('edit/<int:recipeid>', views.Edit, name='edit'),

]