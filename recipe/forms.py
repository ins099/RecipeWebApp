from django import forms
from . models import Category

class NewRecipe(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'id':'title' }))
    ingredients = forms.CharField(label="Ingredients", widget=forms.Textarea(attrs={'class':'form-control', 'id':'ingredients' }), required=False)
    procedure = forms.CharField(label="Procedure", widget=forms.Textarea(attrs={'class':'form-control', 'id':'procedure', 'style': {"height":"1000px"} }), required=False)
    category = forms.ChoiceField(choices=[(i, str(obj)) for i, obj in enumerate(Category.objects.all())], initial= 'Select', label="Category", widget=forms.Select(attrs={
        'class':"form-select" ,'id':"floatingSelect" ,'aria-label':"Floating label select example"
    }))
    img = forms.ImageField(allow_empty_file=True)