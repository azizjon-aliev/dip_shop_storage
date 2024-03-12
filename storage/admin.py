from django.contrib import admin
from .models import Category, Product, Counterparty, OperationGroup, Operation
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
        
        
# use Operation inline for OperationGroup 
class OperationInline(admin.TabularInline):
    model = Operation
    extra = 3
    autocomplete_fields = ('product', )
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'amount', 'action', )
    fields = (
        'product',
        'price',
        'quantity',
        'discount',
    )
    
    
@admin.register(OperationGroup)
class OperationGroup(admin.ModelAdmin):
    """ Административная панель для модели OperationGroup."""
    
    autocomplete_fields = ('counterparty', )
    list_display = ('counterparty', 'action', "created_at", )
    search_fields = ('counterparty__full_name', )
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_filter = ('action', 'counterparty', )
    inlines = [OperationInline, ]
    
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
        
        
@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    """ Административная панель для модели Operation."""
    
    autocomplete_fields = ('product', 'operation_group', )
    list_display = ('product', 'operation_group', 'amount', 'created_at', )
    search_fields = ('product__name', )
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_filter = ('product', 'operation_group', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()