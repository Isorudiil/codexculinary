from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
]