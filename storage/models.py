from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    """Model category for product"""
    
    class Meta:
        ordering = ("-id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
        
    name = models.CharField(verbose_name="Название", max_length=200)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время изменения", auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class Product(models.Model):
    """Model product"""
    
    class Meta:
        ordering = ("-id",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        
    image = models.ImageField(upload_to="products/", verbose_name="Изображение", blank=True, null=True)
    name = models.CharField(verbose_name="Название", max_length=200)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время изменения", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Кто создал", on_delete=models.SET_NULL, related_name="%(class)s_created_by", blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name="Кто изменил", on_delete=models.SET_NULL, related_name="%(class)s_updated_by", blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
    

class Counterparty(models.Model):
    """Model counterparty"""
    
    class Meta:
        ordering = ("-id",)
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        
    full_name = models.CharField(verbose_name="ФИО", max_length=200)
    phone = models.CharField(verbose_name="Телефон", max_length=200)
    company_name = models.CharField(verbose_name="Компания", max_length=255)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время изменения", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Кто создал", on_delete=models.SET_NULL, related_name="%(class)s_created_by", blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name="Кто изменил", on_delete=models.SET_NULL, related_name="%(class)s_updated_by", blank=True, null=True)
    
    def __str__(self) -> str:
        return self.full_name
    
    
class Action(models.IntegerChoices):
    DEBIT = 1, "Дебет"
    CREDIT = 2, "Кредит"

    
class OperationGroup(models.Model):
    """Model operation group"""
    
    class Meta:
        ordering = ("-id",)
        verbose_name = "Группа операций"
        verbose_name_plural = "Группы операций"
        
    counterparty = models.ForeignKey(Counterparty, verbose_name="Контрагент", on_delete=models.CASCADE)
    action = models.IntegerField(verbose_name="Действие", choices=Action.choices)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время изменения", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Кто создал", on_delete=models.SET_NULL, related_name="%(class)s_created_by", blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name="Кто изменил", on_delete=models.SET_NULL, related_name="%(class)s_updated_by", blank=True, null=True)
    
    def __str__(self) -> str:
        return self.counterparty.full_name
    
    
class Operation(models.Model):
    """Model operation"""
    
    class Meta:
        ordering = ("-id",)
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    operation_group = models.ForeignKey(OperationGroup, verbose_name="Группа операций", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    discount = models.DecimalField(verbose_name="Скидка", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Время изменения", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Кто создал", on_delete=models.SET_NULL, related_name="%(class)s_created_by", blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name="Кто изменил", on_delete=models.SET_NULL, related_name="%(class)s_updated_by", blank=True, null=True)
    
    @property
    def amount(self) -> float:
        return self.quantity * self.price * (1 - self.discount / 100)
    
    @property
    def action(self) -> int:
        return self.operation_group.action
    
    def __str__(self) -> str:
        return self.product.name