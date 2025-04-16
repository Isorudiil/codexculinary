from contextlib import nullcontext

from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    """
    Represents a recipe with its details, ingredients, and instructions.
    """
    name = models.CharField(max_length=100)
    ingredient_details = models.JSONField()
    instructions = models.JSONField() # storing as list of instructions
    servings = models.IntegerField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    category = models.JSONField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    )

    DAY_OF_WEEK = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_OF_WEEK)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)