from django.db import models


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
    
    
    
# created_by = models.ForeignKey(
#         "accounts.User",
#         verbose_name="Кто создал",
#         on_delete=models.SET_NULL,
#         related_name="%(class)s_created_by",
#         blank=True,
#         null=True,
#     )
#     updated_by = models.ForeignKey(
#         "accounts.User",
#         verbose_name="Кто изменил",
#         on_delete=models.SET_NULL,
#         related_name="%(class)s_updated_by",
#         blank=True,
#         null=True,
#     )