from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test product to the database"

    def handle(self, *args, **kwargs):
        category, _ = Category.objects.get_or_create(name="Smartphones")

        product = [
            {
                "name": "iphone 15",
                "description": "green color, 256 GB",
                "category": "Smartphones",
            },
            {
                "name": "Xiaomi 14",
                "description": "black edition",
                "category": "Smartphones",
            },
        ]

        for product_data in product:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exists: {product.name}")
                )
