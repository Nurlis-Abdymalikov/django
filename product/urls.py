from django.urls import path
from .views import (
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView,
    ProductsWithReviewsAPIView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-rud'),

    # Products
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-rud'),
    path('products/reviews/', ProductsWithReviewsAPIView.as_view(), name='products-with-reviews'),

    # Reviews
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:id>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-rud'),
]
