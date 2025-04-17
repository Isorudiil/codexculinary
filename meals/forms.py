from django import forms
from .models import Meal
from recipes.models import Recipe

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['recipe', 'day', 'meal_type']