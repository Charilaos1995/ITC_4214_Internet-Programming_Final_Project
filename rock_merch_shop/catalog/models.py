from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    Represents a category for items in the catalog.

    Attributes:
        - name (CharField): The name of the category. Must be unique.

    Methods:
        - __str__(self): Returns a string representation of the category, which is its name.
    """
    # The name of the category. Must be unique.
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """
        Returns a string representation of the Category instance, which is its name.

        :return: The name of the category.
        """
        return self.name

class Band(models.Model):
    """
    Represents a musical band/group in the catalog.

    Attributes:
        - name (CharField): The name of the band. Must be unique.
        - genre (CharField): The genre of the band's music.

    Methods:
        - __str__(self): Returns a string representation of the band, which is its name.
    """
    name = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns a string representation of the Band instance, which is its name.
        :return: The name of the band.
        """
        return self.name

class Item(models.Model):
    """
    Represents an item in the catalog, which could be merchandise related to a band or a musical album.

    Attributes:
        - name (CharField): The name or title of the item.
        - description (TextField): A detailed description of the item.
        - price (DecimalField): The price of the item.
        - category (ForeignKey): A reference to the Category model, indicating which category this item belongs to.
        - band (ForeignKey): A reference to the Band model, indicating the band associated with this item.
        - image (ImageField): An image of the item. Stored in 'item_images/' directory.
        - is_featured (BooleanField): A flag to indicate whether the item is featured on the homepage or not.

    Methods:
        - average_rating(self): Calculates the average rating of the item based on user reviews.
        - total_ratings(self): Returns the total number of ratings the item has received.
        - __str__(self): Returns the name of the item as its string representation.
        """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def average_rating(self):
        """
        Calculates the average rating of the item.

        :return: The average rating as a float, or 0 if the item has no ratings.
        """
        return self.ratings.aggregate(Avg('score'))['score__avg'] or 0

    def total_ratings(self):
        """
        Returns the total number of ratings that the item has received.

        :return: The total number of ratings as an integer.
        """
        return self.ratings.count()

    def __str__(self):
        """
        Returns a string representation of the Item instance, which is its name.

        :return: The name of the item.
        """
        return self.name

class SearchHistory(models.Model):
    """
    Represents a record of a user's search query in the system.

    Attributes:
        - user (ForeignKey): A reference to the User model, indicating which user performed the search.
        - query (CharField): The search query string that was input by the user.
        - timestamp (DateTimeField): The date and time when the search was performed, automatically set to the current time.

    Methods:
        - __str__(self): Returns a string representation of the SearchHistory instance, showing the user and their query.
        """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the SearchHistory instance, including the username and the query.

        :return: A formatted string showing the user's username and their search query.
        """
        return f'{self.user.username}: {self.query}'

class Rating(models.Model):
    """
    Represents a user's rating of an item in the system.

    Attributes:
        - item (ForeignKey): A reference to the Item model, indicating the item that is being rated.
        - user (ForeignKey): A reference to the User model, indicating which user is giving the rating.
        - score (IntegerField): The rating score given by the user, with possible values from 1 to 5.
        - timestamp (DateTimeField): The date and time when the rating was given, automatically set to the current time.

    Meta:
        - unique_together: Ensures that a user can only rate a specific item once.

    Methods:
        - __str__(self): Returns a string representation of the Rating instance, showing the user, item, and score.
        """
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(default=1, choices=[(i, str(i)) for i in range (1, 6)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['item', 'user']

    def __str__(self):
        """
        Returns a string representation of the Rating instance, including the username, item name, and the score.

        :return: A formatted string showing the user's username, the name of the item, and the rating score.
        """
        return f'{self.user.username} rating for {self.item.name}: {self.score}'