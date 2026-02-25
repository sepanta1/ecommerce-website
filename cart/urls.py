from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
    MergeGuestCartView,
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("add/", AddToCartView.as_view(), name="add"),
    path("update/", UpdateCartItemView.as_view(), name="update"),
    path("remove/", RemoveCartItemView.as_view(), name="remove"),
    path("clear/", ClearCartView.as_view(), name="clear"),
    path("merge/", MergeGuestCartView.as_view(), name="merge"),
]
