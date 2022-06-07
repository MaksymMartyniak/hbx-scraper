from django.urls import path, include
from .views import (
    ClothingApiView,
    CategoriesApiView
)

urlpatterns = [
    path('clothing', ClothingApiView.as_view()),
    path('categories', CategoriesApiView.as_view()),
]