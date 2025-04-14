from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm
from .models import Recipe

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, '../templates/recipe_list.html', {'recipes': recipes})