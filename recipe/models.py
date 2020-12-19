from django.db import models
from django.contrib.auth.models import AbstractUser

#create your models here

class User(AbstractUser):
    pass

class Category(models.Model):
    cat = models.CharField(max_length= 50, primary_key=True)
    def __str__(self):
        return self.cat

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'cook')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=False, related_name='category', on_delete=models.CASCADE)
    ingredients = models.TextField(max_length=100000)
    procedure = models.TextField(max_length=100000)
    likes = models.ManyToManyField(User, blank=True, related_name="recipe_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="recipe_dislikes")
    dateposted = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title


class Following(models.Model):
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

	def __str__(self):
		return f"{self.follower} -> {self.following}"