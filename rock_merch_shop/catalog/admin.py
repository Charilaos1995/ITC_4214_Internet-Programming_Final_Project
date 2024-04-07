from django.contrib import admin
from .models import Band, Category, Item

# Register your models here.

# Registers the Band model with the default ModelAdmin
admin.site.register(Band)

# Registers the Category model with the default ModelAdmin
admin.site.register(Category)

# ItemAdmin customizes the admin interface for the Item model
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['name', 'category', 'band', 'price', 'is_featured']
    # Filters to display in the sidebar
    list_filter = ['is_featured', 'category', 'band']
    # Fields that can be searched
    search_fields = ['name']
