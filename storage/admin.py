from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Административная панель для модели Category.
    """
    
    search_fields = ('name', )
    list_display = ('name', 'created_at', )
    readonly_fields = ('created_at', 'updated_at', )
    
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Административная панель для модели Product.
    """
    
    search_fields = ('name', 'category__name', )
    list_display = ('name', 'category', 'created_at', )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', )
    autocomplete_fields = ('category', )
    list_filter = ('category', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
    