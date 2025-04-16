from django.shortcuts import render, redirect, get_object_or_404
from .forms import MealForm, RecipeForm
from .models import Meal, Recipe
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes, 'title': 'Recipe List'}
    return render(request, "recipe_list.html", context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {'recipe': recipe}
    return render(request, "recipe_detail.html", context)

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = Recipe(
                name=form.cleaned_data['name'],
                ingredient_details=form.cleaned_data['ingredient_details'],
                instructions=form.cleaned_data['instructions'],
                servings=form.cleaned_data['servings'],
                prep_time=form.cleaned_data['prep_time'],
                cook_time=form.cleaned_data['cook_time'],
                category=form.cleaned_data['category'],
                notes=form.cleaned_data['notes']
            )
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

@login_required
def meal_schedule(request):
    meals = Meal.objects.filter(user=request.user)
    context = {'meals': meals}
    return render(request, 'recipes/meal_schedule.html', context)

@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('meal_schedule')
    else:
        form = MealForm()
    context = {'form': form}
    return render(request, 'recipes/add_meal.html', context)

@login_required
def edit_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_schedule')
    else:
        form = MealForm(instance=meal)
    context = {'form': form}
    return render(request, 'recipes/edit_meal.html', context)

@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_schedule')
    context = {'meal', meal}
    return render(request, 'recipes/delete_meal.html', context)
