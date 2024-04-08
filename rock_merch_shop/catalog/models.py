from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def average_rating(self):
        return self.ratings.aggregate(Avg('score'))['score__avg'] or 0

    def total_ratings(self):
        return self.ratings.count()

    def __str__(self):
        return self.name

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.query}'

class Rating(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(default=1, choices=[(i, str(i)) for i in range (1, 6)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['item', 'user']

    def __str__(self):
        return f'{self.user.username} rating for {self.item.name}: {self.score}'