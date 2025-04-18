import csv
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, CSVImportForm
from .models import Recipe
from .utils import separate_by_comma, parse_ingredient_details
import re
from fractions import Fraction
import logging

def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes, 'title': 'Recipe List'}
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {'recipe': recipe}
    return render(request, "recipes/recipe_detail.html", context)

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
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe.name = form.cleaned_data['name']
            recipe.ingredient_details = form.cleaned_data['ingredient_details']
            recipe.instructions = form.cleaned_data['instructions']
            recipe.servings = form.cleaned_data['servings']
            recipe.prep_time = form.cleaned_data['prep_time']
            recipe.cook_time = form.cleaned_data['cook_time']
            recipe.category = form.cleaned_data['category']
            recipe.notes = form.cleaned_data['notes']
            form.save()
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        formatted_ingredients = "\n".join(
            f"{name}: {details['quantity']} {details['unit']}"
            for name, details in recipe.ingredient_details.items()    
        )
        formatted_instructions = "\n".join(recipe.instructions)
        formatted_category = ", ".join(recipe.category)
        form = RecipeForm(initial={
            'name': recipe.name,
            'ingredient_details': formatted_ingredients,
            'instructions': formatted_instructions,
            'servings': recipe.servings,
            'prep_time': recipe.prep_time,
            'cook_time': recipe.cook_time,
            'category': formatted_category,
            'notes': recipe.notes,
        })
    context = {'form': form, 'recipe': recipe}
    return render(request, 'recipes/edit_recipe.html', context)

def import_recipes_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                context = {'form': form, 'error': 'File is not CSV type'}
                return render(request, 'recipes/import_csv.html', context)
            
            data = csv_file.read().decode('utf-8')
            csv_data = csv.reader(data.splitlines())

            if form.cleaned_data['has_header']:
                next(csv_data)

            errors = []
            recipes_to_create = []

            for col in csv_data:
                try:
                    name = col[0]
                    ingredients_details_str = col[1]
                    instructions_str = col[2]
                    servings = int(col[3])
                    prep_time = int(col[4])
                    cook_time = int(col[5])
                    category_str = col[6]
                    notes = col[7]

                    ingredient_details = {}
                    ingredients_list = separate_by_comma(ingredients_details_str)
                    print(ingredients_list)
                    for ingredient in ingredients_list:
                        ingredient_details.update(parse_ingredient_details(ingredient))
                    instructions = separate_by_comma(instructions_str)
                    category = separate_by_comma(category_str)

                    recipes_to_create.append(
                        Recipe(
                            name=name,
                            ingredient_details=ingredient_details,
                            instructions=instructions,
                            servings=servings,
                            prep_time=prep_time,
                            cook_time=cook_time,
                            category=category,
                            notes=notes,
                        )
                    )

                except Exception as e:
                    errors.append(f'Error processing row: {e}')
                
            if errors:
                context = {'form': form, 'errors': errors}
                return render(request, 'recipes/import_csv.html', context)
            
            Recipe.objects.bulk_create(recipes_to_create)
            return redirect('recipes:recipe_list')
    else:
        form = CSVImportForm()
    context = {'form': form}
    return render(request, 'recipes/import_csv.html', context)

def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:recipe_list')
    context = {'recipe': recipe}
    return render(request, 'recipes/delete_recipe_confirm.html', context)
