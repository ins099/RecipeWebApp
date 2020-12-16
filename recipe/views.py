from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request , 'recipe/index.html')

def allrecipes(request):
    return render(request , 'recipe/allrecipes.html')
def createrecipe(request):
    return render(request, 'recipe/create.html')