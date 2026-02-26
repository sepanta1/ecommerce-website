# products/views.py

from django.views.generic import DetailView, ListView

from .models import Product,Category


class ProductListView(ListView):
    """
    Display all active products
    """

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True).prefetch_related("images")
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        return context
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
