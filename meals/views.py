from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MealForm
from .models import Meal

@login_required
def meal_schedule(request):
    meals = Meal.objects.filter(user=request.user)
    context = {'meals': meals}
    return render(request, 'meals/meal_schedule.html', context)

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
    return render(request, 'meals/add_meal.html', context)

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
    return render(request, 'meals/edit_meal.html', context)

@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_schedule')
    context = {'meal', meal}
    return render(request, 'meals/delete_meal.html', context)
