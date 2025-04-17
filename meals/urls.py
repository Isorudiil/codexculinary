from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal_schedule),
    path('add/', views.add_meal),
    path('edit/', views.edit_meal),
    path('delete/', views.delete_meal),
]