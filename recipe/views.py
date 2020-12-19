from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Recipe, Category, Following
from .forms import NewRecipe

# Create your views here.
def index(request):
    return render(request , 'recipe/index.html')

def allrecipes(request):
    recipes = Recipe.objects.all()
    recipes = recipes.order_by(*['-dateposted'])
    recipes = recipes.values(*['pk', 'title','category','author','ingredients','procedure', 'dateposted'])
    recipes = list(recipes)
    return JsonResponse(recipes, safe=False)

@login_required
def createrecipe(request):
    if request.method == 'POST':
        form = NewRecipe(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']            
                category_name = dict(form.fields['category'].choices)[int(form.cleaned_data["category"])]
                ingredients = form.cleaned_data['ingredients']
                procedure =  form.cleaned_data['procedure']
                new_recipe = Recipe(title = title,
                                    author = request.user,
                                    category = Category.objects.get(pk = category_name),
                                    ingredients=ingredients,
                                    procedure = procedure,
                                    )
                new_recipe.save()
            except IntegrityError:
                return render(request, 'recipe/create.html',{
                    'form': NewRecipe(request.POST),
                    'message': 'An Error occured, Try again'
                })

            return HttpResponse('form Submitted')
        
        return render(request, 'recipe/create.html', {
        'form': NewRecipe()
    })
    return render(request, 'recipe/create.html', {
        'form': NewRecipe()
    })

def RecipeView(request, id):
    recipe = Recipe.objects.get(pk = id)
    return render(request, 'recipe/recipe.html', {
        'recipe': recipe
    })

def userProfile(request,username):
    context = {}
    userP = User.objects.all().filter(username=username).first()
    recipes = Recipe.objects.filter(author = userP).all()
    followers = Following.objects.filter(following=userP).all().count()
    following = Following.objects.filter(follower = userP).all().count()

    context['recipes'] = recipes
    context['userProfile'] = userP
    context['user_follower'] = followers
    context['user_following'] = following

    # likes = []
    # for recipe in recipes:
    #     likes.append(recipe.likes.all().count())
    # context['likes']=likes

    if request.user.is_authenticated:
        following_status = Following.objects.filter(follower=request.user, following= userP)
        if len(following_status) == 0:
            context['following_state']= 'Follow'
        else:
            context['following_state']= 'UnFollow'

    return render (request, 'recipe/profile.html',context)

def Follow(request):
    if request.method == 'POST':
        person_to_follow = User.objects.filter(username = request.POST['username']).first()
        following_status = Following.objects.all().filter(models.Q(follower=request.user, following=person_to_follow))
        if len(following_status) == 0:
            new_state = Following(follower=request.user, following=person_to_follow)
            new_state.save()
        else:
            Following.objects.get(follower=request.user, following=person_to_follow).delete()

        return HttpResponseRedirect(reverse("profile", args=[request.POST["username"]]))

def like(request):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk = request.POST['like'])
        all_users = recipe.likes.all()

        if request.user not in all_users:
            recipe.likes.add(request.user)
        
        return JsonResponse({'likes':recipe.likes.all().count()})

def dislike(request):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk = request.POST['dislike'])
        all_users = recipe.dislikes.all()

        if request.user not in all_users:
            recipe.dislikes.add(request.user)
        
        return JsonResponse({'dislikes':recipe.dislikes.all().count()})


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


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipe/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipe/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipe/register.html")
