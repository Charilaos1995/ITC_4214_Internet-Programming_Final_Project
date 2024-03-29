from django.contrib import admin
from .models import Band, Category, Item

# Register your models here.
admin.site.register(Band)
admin.site.register(Category)
admin.site.register(Item)