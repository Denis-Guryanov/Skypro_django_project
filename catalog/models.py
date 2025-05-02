from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    description = models.CharField(max_length=150, verbose_name="Описание категории")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название товара")
    description = models.CharField(max_length=150, verbose_name="Описание товара")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение товара", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория товара",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.CharField(max_length=150, verbose_name="Цена товара")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        null=True,
        blank=True,
        related_name="products",
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания товара"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения товара"
    )
    PUBLISH_STATUS = [
        ("moderation", "На модерации"),
        ("published", "Опубликовано"),
        ("unpublished", "Снято с публикации"),
        ("archived", "В архиве"),
    ]
    is_published = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default="moderation",  # Статус по умолчанию
        verbose_name="Статус публикации",
        help_text="Выберите статус публикации",
    )

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"

    @receiver(post_save, sender=Category)
    @receiver(post_delete, sender=Category)
    def clear_category_cache(sender, instance, **kwargs):
        # Сбрасываем кеш для этой категории
        cache.delete(f"products_category_{instance.slug}")

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "price"]
        permissions = [("can_unpublish_product", "Можно отменить публикацию продукта")]
