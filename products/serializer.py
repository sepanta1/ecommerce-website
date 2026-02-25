# from rest_framework import serializers

# from .models import Product


# class ProductSerializer(serializers.ModelSerializer):
#     brand = serializers.StringRelatedField()
#     category = serializers.StringRelatedField()

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "description",
#             "sku",
#             "brand",
#             "category",
#             "price",
#             "stock_quantity",
#             "is_available",
#             "created_at",
#         ]
#         read_only_fields = fields
