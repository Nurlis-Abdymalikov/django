from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from django.db.models import Avg
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, ConfirmSerializer
from django.contrib.auth import get_user_model

@api_view(['GET'])
def category_list_view(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def review_list_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['GET'])
def products_with_reviews_view(request):
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

@api_view(['POST'])
def category_create_view(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def category_update_delete_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)


@api_view(['POST'])
def product_create_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def product_update_delete_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    if request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['POST'])
def review_create_view(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def review_update_delete_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)

    if request.method == 'PUT':
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)

User = get_user_model()

@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'Пользователь зарегистрирован. Подтвердите код.'}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def confirm_user_view(request):
    serializer = ConfirmSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'Пользователь подтвержден.'})
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Пользователь не активен. Подтвердите код.'}, status=403)
    return Response({'error': 'Неверные учетные данные.'}, status=400)