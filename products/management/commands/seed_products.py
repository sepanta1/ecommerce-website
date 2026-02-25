import random

from django.core.management.base import BaseCommand
from django.db import transaction

from products.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductVariantFactory,
)
from products.models import ProductImage


class Command(BaseCommand):
    help = "Seed products app with fake data"

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=5)
        parser.add_argument("--brands", type=int, default=5)
        parser.add_argument("--products", type=int, default=20)
        parser.add_argument("--variants", type=int, default=30)
        parser.add_argument("--images", type=int, default=40)

    @transaction.atomic
    def handle(self, *args, **options):
        categories = CategoryFactory.create_batch(options["categories"])
        brands = BrandFactory.create_batch(options["brands"])

        products = ProductFactory.create_batch(
            options["products"],
            category=random.choice(categories),
            brand=random.choice(brands),
        )

        # images
        for _ in range(options["images"]):
            ProductImageFactory.create(product=random.choice(products))

        # ensure each product has at most 1 primary image
        for p in products:
            img = ProductImage.objects.filter(product=p).first()
            if img:
                img.is_primary = True
                img.save(update_fields=["is_primary"])

        # variants
        for _ in range(options["variants"]):
            ProductVariantFactory.create(product=random.choice(products))

        self.stdout.write(self.style.SUCCESS("Products seeded successfully!"))
