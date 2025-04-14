from django.shortcuts import render, redirect
from .forms import RecipeForm
from .models import Recipe
from rest_framework import generics
from .serializers import RecipeSerializer


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = Recipe(
                name=form.cleaned_data['name'],
                ingredient_names=form.cleaned_data['ingredient_names'],
                ingredient_details=form.cleaned_data['ingredient_details'],
                instructions=form.cleaned_data['instructions'],
                servings=form.cleaned_data['servings'],
                prep_time=form.cleaned_data['prep_time'],
                cook_time=form.cleaned_data['cook_time'],
                category=form.cleaned_data['category'],
                notes=form.cleaned_data['notes'],
            )
            recipe.save()
            return redirect('recipe_list')

    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})