from django.contrib import admin
from .models import Category, Product, Counterparty, OperationGroup, Operation
from django.utils.safestring import mark_safe
from django.db.models import Sum
from .utils import get_remaining_product

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
    list_display = ('name', 'get_remaining',  'show_image', 'category', 'created_at', )
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
    

    def get_remaining(self, obj):
        return get_remaining_product(product=obj)
    
    
    def show_image(self, obj):
        if bool(obj.image):
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
        
    get_remaining.short_description = 'остатка'
    show_image.short_description = 'изображение'
    
    
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
    list_display = ('counterparty', 'quantity_product',  'amount_product', 'action', "created_at", )
    list_filter = ('action', 'counterparty', )
    search_fields = ('counterparty__full_name', )
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    inlines = [OperationInline, ]


    def quantity_product(self, obj) -> int:
        if obj.operation_set.exists():
            return Operation.objects.filter(operation_group=obj).values_list('quantity', flat=True).aggregate(total_quantity=Sum('quantity')).get('total_quantity')
        return 0
    
    def amount_product(self, obj) -> float:
        if obj.operation_set.exists():
            amount = sum([i.amount for i in Operation.objects.filter(operation_group=obj)])
            return round(amount, 2)
        return 0.00

    amount_product.short_description = "Общая сумма товаров"
    quantity_product.short_description = "Количество товаров"
    
    
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()