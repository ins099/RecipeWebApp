from django.db import models
from django.contrib.auth.models import AbstractUser

#create your models here

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to = 'userprofilepic', blank= True, null= True)

    def __str__(self):
        return self.username

class Category(models.Model):
    cat = models.CharField(max_length= 50, primary_key=True)

    def __str__(self):
        return self.cat

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'recipes')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100000)
    category = models.ForeignKey(Category, null=False, related_name='recipes', on_delete=models.CASCADE)
    ingredients = models.TextField(max_length=100000)
    procedure = models.TextField(max_length=100000)
    likes = models.ManyToManyField(User, blank=True, related_name="recipe_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="recipe_dislikes")
    dateposted = models.DateTimeField(auto_now_add= True)
    img = models.ImageField(blank=True, null =True, upload_to = 'recipeimages')
    def __str__(self):
        return self.title


class Following(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

	def __str__(self):
		return f"{self.follower} -> {self.following}"

class Comment(models.Model):
    recipepost= models.ForeignKey(Recipe, on_delete= models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'comments')
    comment = models.TextField(max_length= 1000)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment