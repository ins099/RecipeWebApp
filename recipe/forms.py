
from django.forms import  ModelForm, TextInput
from django.forms.widgets import Textarea, Select
from . models import Recipe
from django import forms

class NewRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'procedure', 'category', 'img']
        widgets = {
            'title': TextInput(attrs={'class':'form-control', 'placeholder':'Enter Title'}),
            'description': Textarea(attrs={'class':'form-control', 'placeholder':'Add a little description about your food','rows':'5' ,
                            'onKeyDown':"limitText(this.form.description,this.form.countdown,250);" ,'onKeyUp':"limitText(this.form.description,this.form.countdown,250);"}),
            'ingredients': Textarea(attrs={'class':'form-control', 'id':'ingredients', 'placeholder':'Enter Ingredients' }),
            'procedure': Textarea(attrs={'class':'form-control', 'id':'procedure', 'placeholder':'Enter Procedure' }),
            'category': Select(attrs={'class':"form-select" ,'id':"floatingSelect" ,'aria-label':"Floating label select example"})
        }

class ProfPic(forms.Form):
    profilephoto = forms.ImageField()