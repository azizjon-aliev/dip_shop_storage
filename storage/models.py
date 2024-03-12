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
        return self.name