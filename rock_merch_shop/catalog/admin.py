from django.contrib import admin
from .models import Band, Category, Item

# Register your models here.
admin.site.register(Band)
admin.site.register(Category)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'band', 'price', 'is_featured']
    list_filter = ['is_featured', 'category', 'band']
    search_fields = ['name']