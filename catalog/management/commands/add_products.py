from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test product to the database"

    def handle(self, *args, **options):
        # Удаляем старую категорию (если существует)
        Category.objects.filter(name="Smartphones").delete()

        # Удаляем старые продукты (если существуют)
        Product.objects.filter(category__name="Smartphones").delete()
        # Получаем или создаем категорию
        category, _ = Category.objects.get_or_create(name="Smartphones")

        # Список данных для продуктов
        products = [
            {
                "name": "iphone 15",
                "description": "green color, 256 GB",
                "category": category,  # Передаем объект категории
            },
            {
                "name": "Xiaomi 14",
                "description": "black edition",
                "category": category,  # Передаем объект категории
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exists: {product.name}")
                )
