import csv
import ast
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, CSVImportForm
from .models import Recipe

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
    print('DEBUG: import_recipes_csv view called')
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            print(f'DEBUG: CSV file name: {csv_file}')
            if not csv_file.name.endswith('.csv'):
                context = {'form': form, 'error': 'File is not CSV type'}
                return render(request, 'recipes/import_csv.html', context)
            
            data = csv_file.read().decode('utf-8')
            csv_data = csv.reader(data.splitlines())

            if form.cleaned_data['has_header']:
                next(csv_data)

            for row in csv_data:
                print(f'DEBUG: Processing row: {row}')
                try:
                    name = row[0]
                    ingredient_details_str = row[1]
                    instructions_str = row[2]
                    servings = int(row[3])
                    prep_time = int(row[4])
                    cook_time = int(row[5])
                    category_str = row[6]
                    notes = row[7]
                    print(f'DEBUG: {name}, {ingredient_details_str}, {instructions_str}, {servings}, {prep_time}, {cook_time}, {category_str}, {notes}')

                    # ingredient_details = ast.literal_eval(ingredient_details_str) if ingredient_details_str else {}
                    # instructions = ast.literal_eval(instructions_str) if instructions_str else []
                    # category = ast.literal_eval(category_str) if category_str else []
                    # print(f'DEBUG: {ingredient_details}, {instructions}, {category}')
                except Exception as e:
                    context = {'form': form, 'error': f'Error processing row: {e}'}
                    return render(request, 'recipes/import_csv.html', )
                
                Recipe.objects.create(
                        name=name,
                        ingredient_details=ingredient_details_str,
                        instructions=instructions_str,
                        servings=servings,
                        prep_time=prep_time,
                        cook_time=cook_time,
                        category=category_str,
                        notes=notes,
                    )
            return redirect('recipes:recipe_list')
    else:
        form = CSVImportForm()
    context = {'form': form}
    return render(request, 'recipes/import_csv.html', context)
