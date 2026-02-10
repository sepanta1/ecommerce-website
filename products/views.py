# products/views.py
from django.db.models import Prefetch, Q
from django.views.generic import DetailView, ListView

from .models import Product, ProductImage


class ProductListView(ListView):
    """
    Display all active products
    """

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10

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

    def get_context_data(self, **kwargs):
        """
        Add related products to context
        Pattern: Context Enhancers (Book Chapter 4, Page 97)
        """
        context = super().get_context_data(**kwargs)

        # Related products from same category
        context["related_products"] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]

        return context
