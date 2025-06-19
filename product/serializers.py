from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым.")
        return value



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название продукта не может быть пустым.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Описание должно быть не короче 10 символов.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Текст отзыва слишком короткий.")
        return value

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Оценка должна быть от 1 до 5.")
        return value

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.generate_confirmation_code()
        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'], confirmation_code=data['code'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный код или имя пользователя.")
        user.is_active = True
        user.confirmation_code = None
        user.save()
        return data