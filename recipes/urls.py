from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('<int:pk>/edit', views.edit_recipe, name='edit_recipe'),
    path('import/csv', views.import_recipes_csv, name='import_recipes_csv')
]