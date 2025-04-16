from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list),
    path('add/', views.add_recipe),
    path('<int:pk>/', views.recipe_detail),
    #path('', views.meal_schedule)
]