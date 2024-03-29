from django.db import models

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
    image = models.ImageField(upload_to='item_images/', blank=True,null=True)

    def __str__(self):
        return self.name