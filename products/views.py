# products/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q, Prefetch
from .models import Product,ProductImage


class ProductListView(ListView):
    """
    Display all active products
    Pattern: Simple ListView (Book Chapter 4)
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_available=True, deleted_at__isnull=True)  # Use filter instead of .active()
            .select_related('category', 'brand')
            .prefetch_related(
                Prefetch(
                    'images',
                    queryset=ProductImage.objects.filter(is_primary=True).order_by('display_order'),
                    to_attr='primary_images'
                )
            )
        )


class ProductDetailView(DetailView):
    """
    Display single product details
    Pattern: DetailView with slug (Book Chapter 4)
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Product.objects
            .active()
            .select_related('category', 'brand')
            .prefetch_related(
                Prefetch(
                    'images',
                    queryset=ProductImage.objects.filter(is_primary=True),
                    to_attr='primary_images'
                )
            )
        )

    def get_context_data(self, **kwargs):
        """
        Add related products to context
        Pattern: Context Enhancers (Book Chapter 4, Page 97)
        """
        context = super().get_context_data(**kwargs)

        # Related products from same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        )[:4]

        return context
