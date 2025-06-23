from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

# --- Category Views ---

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


# --- Product Views ---

class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# --- Review Views ---

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


# --- Products with Reviews and Average Rating ---

class ProductsWithReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = []

        for product in products:
            reviews = product.reviews.all()
            avg_rating = reviews.aggregate(Avg('stars'))['stars__avg']
            data.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category': product.category.name,
                'rating': round(avg_rating, 2) if avg_rating else None,
                'reviews': ReviewSerializer(reviews, many=True).data
            })

        return Response(data)
