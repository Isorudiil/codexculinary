from django.urls import path
from. import views

urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail'),
]