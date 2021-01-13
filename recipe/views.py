
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework import generics

from .models import User, Recipe, Category, Comment
from .forms import NewRecipe, ProfPic
from .serializers import RecipeSerializer
from .decorators import unauthenticated_user

# Create your views here.
def index(request):
    return render(request , 'recipe/index.html',{
        'categories':listcat()
    })

class RecentRecipeView(generics.ListAPIView):

    queryset = Recipe.objects.all().order_by('-dateposted')[:5]
    serializer_class = RecipeSerializer

def AllRecipes(request):
    recipes = Recipe.objects.all().order_by('-dateposted')
        
    return render(request, 'recipe/allrecipes.html', {
        'recipes':recipes,
        'categories':listcat(),
    })

def search(request):
    if request.method == 'POST':
        s_value = request.POST.get('search')
        if s_value:
            results = Recipe.objects.filter(title__contains = s_value)
            return render (request, 'recipe/search.html', {
                'value':s_value,
                'results':results,
                'exists': len(results),
                'categories':listcat()
            })


@login_required
def createrecipe(request):
    if request.method == 'POST':
        form = NewRecipe(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                
                f = form.save(commit=False)
                f.author = request.user
                f.save()
                return HttpResponseRedirect(reverse('recipeid', args= [f.id]))
                

            except IntegrityError:
                return render(request, 'recipe/create.html',{
                    'form': NewRecipe(request.POST),
                    'message': 'An Error occured, Try again'
                })

        return render(request, 'recipe/create.html', {
        'form': NewRecipe(),
        'categories':listcat(),
        'message':"Form Validation error!!!"
    })
    return render(request, 'recipe/create.html', {
        'form': NewRecipe(),
        'categories':listcat()
    })

def ListCategory(request):
    context = {}
    category = Category.objects.get(pk = request.GET.get('selected'))
    context['category'] = category
    context['recipes'] = category.recipes.all()
    context['categories'] = Category.objects.all()
    return render (request, 'recipe/category.html', context)     

def RecipeView(request, id):
    recipe = get_object_or_404(Recipe,pk = id)
    print(recipe.comments.all())

    likes = []
    likes.append(recipe.likes.all().count())

    return render(request, 'recipe/recipe.html', {
        'recipe': recipe,
        'comments':recipe.comments.all(),
        'likes':likes[0],
        'categories':listcat()
    })

def userProfile(request,username):

    context = {}
    if User.objects.filter(username = username).exists():
        context['categories']=listcat()

        userP = User.objects.all().filter(username=username).first()
        recipes = Recipe.objects.filter(author = userP).all().order_by('-dateposted')
        existPhoto = get_object_or_404(User, username = username)
        existPhoto = str(existPhoto.profile_pic)
        print(len(existPhoto))
        if len(existPhoto) > 0:
            context['exists'] = True
        else:
            context['exists'] = False 

        if request.method == 'POST':
            form = ProfPic(data=request.POST, files = request.FILES)
            if form.is_valid():
                profilePicture = form.cleaned_data['profilephoto']
                user = get_object_or_404(User, username = username)
                user.profile_pic = profilePicture
                user.save(update_fields=['profile_pic'])
                print(profilePicture)
                return HttpResponseRedirect(reverse('profile', args = [userP]))
            else:
                context["form"] = ProfPic()
                context["message"] = "Form Validation Error"
        
        context['form'] = ProfPic()

        if len(recipes) != 0: 
            context['recipes'] = recipes
            context['userProfile'] = userP
            context['categories'] = listcat()
            context['comments'] = Comment.objects.all()
            
            likes = []
            for recipe in recipes:
                likes.append(recipe.likes.all().count())
            
            context['likes']=likes[0]

            return render (request, 'recipe/profile.html',context)
        else:
            context['recipes'] = recipes
            context['userProfile'] = userP
            
            if request.user != userP:
                context['norecipes'] = f"{username.upper()} has No recipes yet!!"
            else:
                context['norecipes'] = f" You donot have any recipes yet!!"
                context['add'] = True


            return render (request, 'recipe/profile.html',context)
    else:
        return HttpResponseNotFound()

def like(request):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk = request.POST['like'])
        all_users = recipe.likes.all()

        if request.user not in all_users:
            recipe.likes.add(request.user)
        else:
            recipe.likes.remove(request.user)
        
        likes = recipe.likes.all().count()

        return HttpResponseRedirect(reverse('recipeid', args=[request.POST['like']]))

@login_required
def CommentSubmit(request):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk = request.POST['recipeid'])
        comment = request.POST['comment']

        print(request.POST)

        new_comment = Comment(author = request.user,
                            recipepost = recipe,
                            comment = comment)
        new_comment.save()

        return HttpResponseRedirect(reverse('recipeid', args = [request.POST['recipeid']]))

@login_required
def Edit(request, recipeid):
    recipe = Recipe.objects.get(pk = recipeid)
    form = NewRecipe(instance=recipe)
    if request.method == 'POST':
        form = NewRecipe(request.POST, request.FILES,instance = recipe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('recipeid', args = [recipeid]))

    return render(request, 'recipe/create.html',{
        'form':form
    })

@login_required
def Delete(request,recipeid):
    recipe = Recipe.objects.get(id= recipeid)
    if request.method == 'POST':
        recipe.delete()
        return HttpResponseRedirect(reverse('profile', args=[recipe.author]))

    return render (request, 'recipe/delete.html', {
        'item':recipe
    })

def listcat():
    categories = Category.objects.all()
    return categories

@unauthenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "recipe/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipe/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@unauthenticated_user
def register(request):
    if request.method == "POST":
        mail = request.POST["email"]
        first = request.POST['first_name']
        last = request.POST['last_name']

        # Ensure password matches confirmation
        passs = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if passs != confirmation:
            return render(request, "recipe/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(request.POST["username"], email=mail, password=passs, first_name=first, last_name=last)
            user.save()
        except IntegrityError:
            return render(request, "recipe/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("profile", args = [user.username]))
    else:
        return render(request, "recipe/register.html")
