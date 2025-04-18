import csv
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, CSVImportForm
from .models import Recipe
from . import utils
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

            start = 1

            if form.cleaned_data['has_header']:
                start = 2
                next(csv_data)

            errors = []
            successful_imports = 0


            for i, row in enumerate(csv_data, start=start):
                try:
                    name = row[0]
                    ingredients_details_str = row[1]
                    instructions_str = row[2]
                    servings = int(row[3])
                    prep_time = int(row[4])
                    cook_time = int(row[5])
                    category_str = row[6]
                    notes = row[7]

                    if Recipe.objects.filter(name=name).exists():
                        errors.append(f'Recipe with name: {name} already exists. Skipping row {i}.')
                        continue

                    ingredient_details = {}
                    ingredients_list = utils.separate_by_comma(ingredients_details_str)
                    for ingredient in ingredients_list:
                        ingredient_details.update(utils.parse_ingredient_details(ingredient))
                    instructions = utils.separate_by_semicolon(instructions_str)
                    category = utils.separate_by_comma(category_str)

                    try:
                        Recipe.objects.create(
                            name=name,
                            ingredient_details=ingredient_details,
                            instructions=instructions,
                            servings=servings,
                            prep_time=prep_time,
                            cook_time=cook_time,
                            category=category,
                            notes=notes,
                        )
                        successful_imports += 1
                    except Exception as create_error:
                        errors.append(f"Error creating recipe in row {i}: {create_error}")

                except Exception as e:
                    errors.append(f'Error processing row: {i}: {e}')
                
            if errors:
                context = {'form': form, 'errors': errors, 'successful_imports': successful_imports}
                return render(request, 'recipes/import_csv.html', context)
            else:
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
