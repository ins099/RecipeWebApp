from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import User, Recipe, Category, Following, Comment
from .forms import NewRecipe, ProfPic
from .serializers import RecipeSerializer

# Create your views here.
def index(request):
    return render(request , 'recipe/index.html',{
        'categories':listcat()
    })

class RecentRecipeView(generics.ListAPIView):
    queryset = Recipe.objects.all().order_by('-dateposted')
    serializer_class = RecipeSerializer

def AllRecipes(request):
    recipes = Recipe.objects.all()
        
    return render(request, 'recipe/allrecipes.html', {
        'recipes':recipes,
        'categories':listcat(),
    })

def search(request):
    pass

@login_required
def createrecipe(request):
    if request.method == 'POST':
        form = NewRecipe(data=request.POST, files = request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']            
                category_name = dict(form.fields['category'].choices)[int(form.cleaned_data["category"])]
                description = form.cleaned_data['description']
                ingredients = form.cleaned_data['ingredients']
                procedure =  form.cleaned_data['procedure']
                image = form.cleaned_data['img']
                new_recipe = Recipe(title = title,
                                    author = request.user,
                                    description = description,
                                    category = Category.objects.get(pk = category_name),
                                    ingredients=ingredients,
                                    procedure = procedure,
                                    img = image,
                                    )
                #for edit save
                if form.cleaned_data['edit']== True:
                    new_recipe.save()
                    return HttpResponseRedirect(reverse('recipeid', kwargs={'id':new_recipe.id}))

                # for new recipe save
                else:
                    new_recipe.save()
                    return HttpResponseRedirect(reverse('recipeid', kwargs={'id':new_recipe.id}))
                

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
    if request.method == 'POST':
        category = Category.objects.get(pk = request.POST['selected'])
        context['category'] = category
        context['recipes'] = category.recipes.all()
    context['categories'] = Category.objects.all()
    return render (request, 'recipe/category.html', context)     

def RecipeView(request, id):
    recipe = Recipe.objects.get(pk = id)
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
        recipes = Recipe.objects.filter(author = userP).all()
        followers = Following.objects.filter(following=userP).all().count()
        following = Following.objects.filter(follower = userP).all().count()
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
            else:
                context["form"] = ProfPic()
                context["message"] = "Form Validation Error"
        
        context['form'] = ProfPic()

        if len(recipes) != 0: 
            context['recipes'] = recipes
            context['userProfile'] = userP
            context['user_follower'] = followers
            context['user_following'] = following
            context['categories'] = listcat()
            context['comments'] = Comment.objects.all()
            
            likes = []
            for recipe in recipes:
                likes.append(recipe.likes.all().count())
            
            context['likes']=likes[0]

            if request.user.is_authenticated:
                following_status = Following.objects.filter(follower=request.user, following= userP)
                if len(following_status) == 0:
                    context['following_state']= 'Follow'
                else:
                    context['following_state']= 'UnFollow'

            return render (request, 'recipe/profile.html',context)
        else:
            context['recipes'] = recipes
            context['userProfile'] = userP
            context['user_follower'] = followers
            context['user_following'] = following
            context['norecipes'] = f"{username.upper()} has No recipes yet!!"
            
            if request.user.is_authenticated:
                following_status = Following.objects.filter(follower=request.user, following= userP)
                if len(following_status) == 0:
                    context['following_state']= 'Follow'
                else:
                    context['following_state']= 'UnFollow'

            return render (request, 'recipe/profile.html',context)
    else:
        return HttpResponseNotFound()

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
        else:
            recipe.likes.remove(request.user)
        
        likes = recipe.likes.all().count()

        return HttpResponseRedirect(reverse('recipeid', args=[request.POST['like']]))

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

def Edit(request, recipeid):
    if request.method=='GET':
        recipe = get_object_or_404(Recipe, pk = recipeid)
        form = NewRecipe()
        form.fields['title'].initial = recipe.title
        form.fields['description'].initial = recipe.description
        form.fields['ingredients'].initial = recipe.ingredients
        form.fields['procedure'].initial = recipe.procedure
        form.fields['category'].initial = recipe.category
        form.fields['img'].initial = recipe.img
        form.fields['edit'].initial = True

        return render(request, 'recipe/create.html',{
            'form':form
        })


def listcat():
    categories = Category.objects.all()
    return categories
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
