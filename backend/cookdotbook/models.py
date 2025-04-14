from contextlib import nullcontext

from django.db import models

class Recipe(models.Model):
    """
    Represents a recipe with its details, ingredients, and instructions.
    """
    name = models.CharField(max_length=100)
    ingredient_names = models.JSONField()
    ingredient_details = models.JSONField()
    instructions = models.JSONField() # storing as list of instructions
    servings = models.IntegerField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    category = models.JSONField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


