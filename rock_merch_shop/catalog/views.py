from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Item, Band
from .models import SearchHistory


# Create your views here.

# Home Page View
def home(request):
    featured_items = Item.objects.filter(is_featured=True)  # Gets only items marked as featured
    categories = Category.objects.all()
    context = {
        'featured_items': featured_items,
        'categories': categories
    }
    return render(request, 'catalog/home.html', context)

# Category List View
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/category_list.html', {'categories': categories})



# Item List View
def item_list(request, category_id=None):
    if category_id:
        items = Item.objects.filter(category=category_id)
    else:
        items = Item.objects.all()
    return render(request, 'catalog/item_list.html', {'items': items})

# Item Detail View
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'catalog/item_detail.html', {'item': item})

# Search Results View
def search_results(request):
    query = request.GET.get('q', '')

    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(band__name__icontains=query)
        ).distinct()

        # Log the search query for authenticated users
        if request.user.is_authenticated:
            log_search_history(request.user, query)
    else:
        items = Item.objects.none()

    context = {'items' : items, 'query': query}
    return render(request, 'catalog/search_results.html', context)

def log_search_history(user, query):
    try:
        search_history = SearchHistory.objects.create(user=user, query=query)
    except Exception as e:
        pass

def search_history(request):
    if not request.user.is_authenticated:
        pass

    # Retrieve search history for the current user
    user_search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'search_history': user_search_history
    }
    return render(request, 'catalog/search_history.html', context)

# Band Detail View
def band_detail(request, band_id):
    band = get_object_or_404(Band, id=band_id)
    items = Item.objects.filter(band=band)
    return render(request, 'catalog/band_detail.html', {'band': band, 'items': items})