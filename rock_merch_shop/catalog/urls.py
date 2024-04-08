from django.urls import path
from . import views
from .views import search_history, submit_rating

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('items/<int:category_id>/', views.item_list, name='item_list'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('search/', views.search_results, name='search_results'),
    path('band/<int:band_id>/', views.band_detail, name='band_detail'),
    path('search-history/', search_history, name='search_history'),
    path('rate/', submit_rating, name='submit_rating'),
]