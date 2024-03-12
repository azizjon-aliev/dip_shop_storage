from django.contrib import admin
from .models import Category, Product, Counterparty
from django.utils.safestring import mark_safe


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
    list_display = ('name', 'show_image', 'category', 'created_at', )
    readonly_fields = ('show_image', 'created_at', 'updated_at', 'created_by', 'updated_by', )
    autocomplete_fields = ('category', )
    list_filter = ('category', )
    fieldsets = (
        ('Информация', {
            "fields": (
                'show_image',
                "image",
                "name",
                "description",
                "category",
            )},
        ),
        ("Время", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
        ("Автор", {
            "fields": (
                "created_by",
                "updated_by",
            ),
        }),
    )
    

    def show_image(self, obj):
        if bool(obj.image):
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
        
    show_image.short_description = 'Изображение'
    
    
@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    """ Административная панель для модели Counterparty.
    """
    
    list_display = ('full_name', 'phone', 'company_name', 'created_at', )
    search_fields = ('full_name', 'phone', 'company_name', )
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    fieldsets = (
        ('Информация', {
            "fields": (
                "full_name",
                "phone",
                "company_name",
            )},
        ),
        ("Время", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
        ("Автор", {
            "fields": (
                "created_by",
                "updated_by",
            ),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()