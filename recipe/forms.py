
from django.forms import  ModelForm, TextInput
from django.forms.widgets import Textarea, Select
from . models import Recipe
from django import forms

# class NewRecipe(forms.Form):
#     title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'id':'title','placeholder':'Enter Title' }))
#     description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Add a little description about your food',
#     'onKeyDown':"limitText(this.form.description,this.form.countdown,150);" ,'onKeyUp':"limitText(this.form.description,this.form.countdown,150);"
#     }))
#     ingredients = forms.CharField(label="Ingredients", widget=forms.Textarea(attrs={'class':'form-control', 'id':'ingredients', 'placeholder':'Enter Ingredients' }))
#     procedure = forms.CharField(label="Procedure", widget=forms.Textarea(attrs={'class':'form-control', 'id':'procedure', 'placeholder':'Enter Procedure', 'style': {"height":"1000px"} }))
#     category = forms.ChoiceField(choices=[(i, str(object)) for i, object in enumerate(Category.objects.all())], initial= 'Select', label="Category", widget=forms.Select(attrs={
#         'class':"form-select" ,'id':"floatingSelect" ,'aria-label':"Floating label select example"
#     }))
#     img = forms.ImageField()
#     edit = forms.BooleanField(initial=False, widget= forms.HiddenInput(), required=False)

class NewRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'procedure', 'category', 'img']
        widgets = {
            'title': TextInput(attrs={'class':'form-control', 'placeholder':'Enter Title'}),
            'description': Textarea(attrs={'class':'form-control', 'placeholder':'Add a little description about your food','rows':'5' ,
                            'onKeyDown':"limitText(this.form.description,this.form.countdown,150);" ,'onKeyUp':"limitText(this.form.description,this.form.countdown,150);"}),
            'ingredients': Textarea(attrs={'class':'form-control', 'id':'ingredients', 'placeholder':'Enter Ingredients' }),
            'procedure': Textarea(attrs={'class':'form-control', 'id':'procedure', 'placeholder':'Enter Procedure' }),
            'category': Select(attrs={'class':"form-select" ,'id':"floatingSelect" ,'aria-label':"Floating label select example"})
        }

class ProfPic(forms.Form):
    profilephoto = forms.ImageField()