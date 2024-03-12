from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Административная панель для модели Category.
    """
    
    list_display = ('name', 'created_at', )
    readonly_fields = ('created_at', 'updated_at', )