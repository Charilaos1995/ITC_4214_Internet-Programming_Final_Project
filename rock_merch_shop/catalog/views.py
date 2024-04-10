from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Item, Band, Rating
from .models import SearchHistory

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.urls import reverse

# Home View
def home(request):
    """
    View function for home page of site.

    Retrieves the featured items, all categories, and all bands to display on the home page.

    :param request: The incoming HTTP request
    :return: Rendered home page with context data
    """
    # Query all items marked as featured for display.
    featured_items = Item.objects.filter(is_featured=True)  # Gets only items marked as featured

    # Query all categories for display in category section.
    categories = Category.objects.all()
    # Query all bands for display in band section.
    bands = Band.objects.all()

    # Prepare context with the queried data.
    context = {
        'featured_items': featured_items,
        'categories': categories,
        'bands': bands
    }

    # Render and return the home page with context.
    return render(request, 'catalog/home.html', context)


# Category List View
def category_list(request):
    """
    View function for listing all categories in the site.

    :param request: The incoming HTTP request.
    :return: Rendered category list page with context data containing all categories.
    """
    # Retrieve all category records from the database.
    categories = Category.objects.all()

    # Context dictionary to be filled with category data for the template.
    context = {'categories': categories}

    # Render and return the category list page with context data.
    return render(request, 'catalog/category_list.html', context)


# Item List View
def item_list(request, category_id=None):
    """
    View function for listing all items or items within a specific category.

    :param request: The incoming HTTP request.
    :param category_id: The ID of the category to filter items by, defaults to None.
    :return: Rendered item list page with context data containing items, optionally filtered by category.
    """
    # Check if a category ID is provided and filter items by category, otherwise retrieve all items.
    items = Item.objects.filter(category=category_id) if category_id else Item.objects.all()

    # Context dictionary to be filled with item data for the template.
    context = {'items': items}

    # Render and return the item list page with the context.
    return render(request, 'catalog/item_list.html', context)


# Item Detail View
def item_detail(request, item_id):
    """
    View function for displaying the detail of a single item.

    If the user is authenticated, it also checks if the user has already rated the item
    and passes that rating to the template for displaying the user's previous rating.

    :param request: The HttpRequest object for the current request.
    :param item_id: The ID of the item to display.
    :return: Rendered item detail page with context data containing the item and user rating.
    """
    # Retrieve the item by ID or return a 404 error if not found.
    item = get_object_or_404(Item, id=item_id)

    # Initialize user_rating as None. It will be updated if the user has a rating for this item.
    user_rating = None

    if request.user.is_authenticated:
        # Query the Rating model for a rating by the current user on this item.
        user_rating_query = Rating.objects.filter(user=request.user, item=item)
        if user_rating_query.exists():
            # If the rating exists, retrieve the score for the user's rating.
            user_rating = user_rating_query.first().score

    # Compile the context with the item, a range for stars (for rating display), and the user's rating (if any).
    context = {
        'item': item,
        'stars_range': range(1, 6), # Provides a range from 1 to 5 for displaying rating stars.
        'user_rating': user_rating  # The user's previous rating, if it exists.
    }

    # Render the 'item_detail.html' template with the provided context.
    return render(request, 'catalog/item_detail.html', context)


# Search Results View
def search_results(request):
    """
    View function for displaying the search results based on a user's query.

    This function retrieves items that match the search query across multiple fields (name, category, band).
    If the user is authenticated, their search is logged for future reference.

    :param request: The HttpRequest object containing the search query.
    :return: HttpResponse object with the rendered search results page.
    """
    # Extract query from GET parameters, defaulting to an empty string if not provided.
    query = request.GET.get('q', '')

    if query:
        # Perform a case-insensitive search across name, category name, and band name.
        # Used 'distinct()' to avoid duplicate items in results.
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(band__name__icontains=query)
        ).distinct()

        # For authenticated users, log the search query for analytics or personalized features.
        if request.user.is_authenticated:
            log_search_history(request.user, query)
    else:
        # If no query is provided, return an empty QuerySet.
        items = Item.objects.none()

    # Compile the context with the items found and the original query string.
    context = {'items': items, 'query': query}

    # Render the 'search_results.html' template with the context.
    return render(request, 'catalog/search_results.html', context)


def log_search_history(user, query):
    """
    Logs the search query made by a user.

    Attempts to create a new SearchHistory object with the user and their search query.
    In case of any exception (e.g., database issues), the error is silently ignored.

    :param user: The User object representing the currently logged-in user.
    :param query: The search query string input by the user.
    """
    try:
        # Attempt to create and save a new search history record.
        SearchHistory.objects.create(user=user, query=query)
    except Exception as e:
        # Log the exception to the server's log.
        print(f"Error logging search history for user {user.username}: {str(e)}")


def search_history(request):
    """
    View function to display the search history of the authenticated user.

    If the user is not authenticated, they are redirected to the login page.

    :param request: HttpRequest object.
    :return: HttpResponse object with the search history page or a redirection.
    """
    if not request.user.is_authenticated:
        # Redirect unauthenticated users to the login page
        return HttpResponseRedirect(reverse('login'))

    # Retrieve search history for the current user, ordered by the timestamp in descending order.
    user_search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')

    # Prepare the context with the search history data.
    context = {
        'search_history': user_search_history
    }

    # Render the 'search_history.html' template with the context.
    return render(request, 'catalog/search_history.html', context)

# Band List View
def band_list(request):
    """
     View function for listing all bands available in the database.

    :param request: HttpRequest object.
    :return: HttpResponse object with the rendered band list page.
    """
    # Retrieve all band records from the database.
    bands = Band.objects.all()

    # Render the 'band_list.html' template with the context containing all bands.
    return render(request, 'catalog/band_list.html', {'bands': bands})

# Band Detail View
def band_detail(request, band_id):
    """
    View function for displaying details about a specific band, including a list of items associated with the band.

    Retrieves the Band object based on the provided band_id. If no Band object is found, a 404 error is raised. Then,
    retrieves all Item objects associated with the band and passes them to the 'band_detail.html' template for
    rendering.

    :param request: HttpRequest object.
    :param band_id: The primary key (ID) of the Band object to be detailed.
    :return: HttpResponse object with the band detail page.
    """

    # Retrieve the band by ID or return a 404 error if not found.
    band = get_object_or_404(Band, id=band_id)

    # Retrieve all items associated with the band.
    items = Item.objects.filter(band=band)

    # Render the 'band_detail.html' template with the band and items context.
    return render(request, 'catalog/band_detail.html', {'band': band, 'items': items})


@login_required
def submit_rating(request):
    """
     Submits a rating for an item by a logged-in user. It either creates a new rating or updates an existing one.

     Only POST requests are accepted. The function expects 'item_id' and 'score' in the POST data. If either is missing,
     or the request method is not POST, it returns a bad request response. This function is decorated with
     @login_required, ensuring that only authenticated users can submit ratings.

    :param request: HttpRequest object, contains 'item_id' and 'score' in POST data.
    :return: JsonResponse indicating the success or failure of the rating submission.
    """

    # Only accept POST requests
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    user = request.user
    item_id = request.POST.get('item_id')
    score = request.POST.get('score')

    # Ensure both item_id and score are provided
    if not item_id or not score:
        # Return a bad request response if either item_id or score is missing
        return HttpResponseBadRequest("Missing item_id or score in POST data.")

    # Attempt to retrieve the item; if not found, respond with error
    try:
        item = get_object_or_404(Item, pk=item_id)
    except Item.DoesNotExist:
        # Return a JSON response with an error message if the item does not exist
        return JsonResponse({'success': False, 'error': "Item does not exist."})

    print(f"Rating Item: {item} with Score: {score} by User: {user.username}")  # Debug print

    # Attempt to create or update the rating
    try:
        # Get or create the rating for the user-item pair
        rating, created = Rating.objects.get_or_create(user=user, item=item, defaults={'score': score})
        if not created:
            # Update the score if the rating already exists
            rating.score = score
            rating.save()
        # Return a success response with the score and item_id
        return JsonResponse({'success': True, 'score': score, 'item_id': item_id})
    except Exception as e:
        # Return an error response if an exception occurs
        return JsonResponse({'success': False, 'error': str(e)})
