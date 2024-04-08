from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Item, Band, Rating
from .models import SearchHistory

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseBadRequest


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
    user_rating = None

    if request.user.is_authenticated:
        # Check if the user has already rated this item
        user_rating_query = Rating.objects.filter(user=request.user, item=item)
        if user_rating_query.exists():
            user_rating = user_rating_query.first().score

    context = {
        'item': item,
        'stars_range': range(1, 6),
        'user_rating': user_rating
    }
    return render(request, 'catalog/item_detail.html', context)


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

    context = {'items': items, 'query': query}
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


@login_required
def submit_rating(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    user = request.user
    item_id = request.POST.get('item_id')
    score = request.POST.get('score')

    if not item_id or not score:
        return HttpResponseBadRequest("Missing item_id or score in POST data.")

    try:
        item = get_object_or_404(Item, pk=item_id)
    except Item.DoesNotExist as e:
        print(f"Item with id {item_id} does not exist.")
        return JsonResponse({'success': False, 'error': str(e)})

    print(f"Rating Item: {item} with Score: {score} by User: {user.username}")  # Debug print

    try:
        rating, created = Rating.objects.get_or_create(user=user, item=item, defaults={'score': score})

        if not created:
            # Update the score if the rating already exists
            rating.score = score
            rating.save()
            print(f"Updated Rating: {rating}")
        else:
            print(f"Created Rating: {rating}")

        return JsonResponse({'success': True, 'score': score, 'item_id': item_id})
    except Exception as e:
        print(f"Error while saving rating: {e}")  # Debug print
        return JsonResponse({'success': False, 'error': str(e)})
