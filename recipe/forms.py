from django import forms
from . models import Category

class NewRecipe(forms.Form):
    title = forms.CharField(max_length=50)
    ingredients = forms.CharField(label="Ingredients", widget=forms.Textarea, required=False)
    procedure = forms.CharField(label="Procedure", widget=forms.Textarea, required=False)
    category = forms.ChoiceField(choices=[(i, str(obj)) for i, obj in enumerate(Category.objects.all())], label="Category")