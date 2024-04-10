from django.urls import path
from . import views
from .views import search_history, submit_rating, band_list

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('categories/', views.category_list, name='category_list'),  # List of categories
    path('items/<int:category_id>/', views.item_list, name='item_list'),  # List of items in a category
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),  # Item detail page
    path('search/', views.search_results, name='search_results'),  # Search results page
    path('band/<int:band_id>/', views.band_detail, name='band_detail'),  # Band detail page
    path('bands/', band_list, name='band_list'),  # List of bands
    path('search-history/', search_history, name='search_history'),  # Search history page
    path('rate/', submit_rating, name='submit_rating'),  # Rating submission
]
