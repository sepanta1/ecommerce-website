# products/views.py
from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    """
    Display all active products
    """

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.prefetch_related("images")


class ProductDetailView(DetailView):
    """
    Display single product details
    """

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.prefetch_related("images")
