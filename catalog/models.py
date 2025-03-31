from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    description = models.CharField(max_length=150, verbose_name="Описание категории")

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
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания товара"
    )
    updated_at = models.DateField(
        auto_now_add=True, verbose_name="Дата последнего изменения товара"
    )

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "price"]
