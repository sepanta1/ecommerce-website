import random
from decimal import Decimal

import factory
from django.utils.text import slugify
from factory import Faker

from products.models import Brand, Category, Product, ProductImage, ProductVariant


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("word")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = Faker("sentence")
    parent = None
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = Faker("sentence")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("sentence", nb_words=3)
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    description = Faker("paragraph")
    sku = factory.Sequence(lambda n: f"SKU-{n:06d}")
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)

    price = factory.LazyFunction(lambda: Decimal(random.randint(1000, 100000)) / 100)
    cost_price = factory.LazyAttribute(
        lambda o: (o.price * Decimal("0.6")).quantize(Decimal("0.01"))
    )
    stock_quantity = factory.LazyFunction(lambda: random.randint(0, 200))
    is_available = True
    meta_description = Faker("sentence")
    meta_keywords = Faker("words", nb=5)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = "products/default.jpg"
    alt_text = Faker("sentence")
    is_primary = False
    display_order = factory.Sequence(lambda n: n)


class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    name = Faker("word")
    sku = factory.Sequence(lambda n: f"VAR-{n:06d}")
    price_adjustment = factory.LazyFunction(
        lambda: Decimal(random.randint(-500, 2000)) / 100
    )
    stock_quantity = factory.LazyFunction(lambda: random.randint(0, 100))
