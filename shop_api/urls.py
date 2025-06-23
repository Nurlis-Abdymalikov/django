from django.contrib import admin
from django.urls import path, include
from product import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/users/', include('users.urls')),

    # Categories
    path('api/v1/categories/', views.category_list_view),
    path('api/v1/categories/create/', views.category_create_view),
    path('api/v1/categories/<int:id>/', views.category_update_delete_view),

    # Products
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/create/', views.product_create_view),
    path('api/v1/products/<int:id>/', views.product_update_delete_view),
    path('api/v1/products/reviews/', views.products_with_reviews_view),

    # Reviews
    path('api/v1/reviews/', views.review_list_view),
    path('api/v1/reviews/create/', views.review_create_view),
    path('api/v1/reviews/<int:id>/', views.review_update_delete_view),
]
