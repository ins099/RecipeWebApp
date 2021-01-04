
from django.forms import widgets
from django import forms
from . models import Category, User

class NewRecipe(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'id':'title','placeholder':'Enter Title' }))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Add a little description about your food',
    'onKeyDown':"limitText(this.form.description,this.form.countdown,150);" ,'onKeyUp':"limitText(this.form.description,this.form.countdown,150);"
    }))
    ingredients = forms.CharField(label="Ingredients", widget=forms.Textarea(attrs={'class':'form-control', 'id':'ingredients', 'placeholder':'Enter Ingredients' }))
    procedure = forms.CharField(label="Procedure", widget=forms.Textarea(attrs={'class':'form-control', 'id':'procedure', 'placeholder':'Enter Procedure', 'style': {"height":"1000px"} }))
    category = forms.ChoiceField(choices=[(i, str(object)) for i, object in enumerate(Category.objects.all())], initial= 'Select', label="Category", widget=forms.Select(attrs={
        'class':"form-select" ,'id':"floatingSelect" ,'aria-label':"Floating label select example"
    }))
    img = forms.ImageField()
    edit = forms.BooleanField(initial=False, widget= forms.HiddenInput(), required=False)

class ProfPic(forms.Form):
    profilephoto = forms.ImageField()