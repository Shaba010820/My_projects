from django.utils.timezone import localtime
from rest_framework import serializers
from .models import (
                     Category,
                     Cart,
                     Sale,
                     Tag,
                     Product,
                     CustomUser,
                     Review,
                     Specification,
                     ProductImage,
                     Order,
                     CartItem,
                     OrderProduct,
                     Profile,
                     Avatar)


class PaymentSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=100)
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    code = serializers.CharField(max_length=3)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class SubcategorySerializer(serializers.ModelSerializer):
    image = ProductImageSerializer()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']


class CategorySerializer(serializers.ModelSerializer):
    image = ProductImageSerializer()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'product']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user  # Получаем текущего авторизованного пользователя
        product = validated_data.get('product')

        # Создаем объект отзыва с автором и остальными данными
        review = Review.objects.create(
            author=user,  # Устанавливаем автора
            email=validated_data.get('email'),
            text=validated_data.get('text'),
            rate=validated_data.get('rate'),
            product=product
        )
        return review


class CatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'freeDelivery', 'images', 'tags', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()


class SaleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Sale
        fields = ('id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'tags', 'title', 'description',
            'fullDescription', 'freeDelivery', 'images', 'tags', 'reviews', 'specifications', 'rating'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        # Проверяем, существует ли уже пользователь с таким же email
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_username(self, value):
        # Проверяем, существует ли уже пользователь с таким же username
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")
        return value


class BasketProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id', allow_null=True)
    category = serializers.IntegerField(source='product.category.id', allow_null=True)
    title = serializers.CharField(source='product.title', allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', allow_null=True)
    description = serializers.CharField(source='product.description', allow_null=True)
    freeDelivery = serializers.BooleanField(source='product.freeDelivery', allow_null=True)
    images = ProductImageSerializer(source='product.images', many=True, allow_null=True)
    tags = TagSerializer(source='product.tags', many=True, allow_null=True)
    count = serializers.IntegerField()
    date = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'category', 'title', 'price', 'count', 'date', 'description', 'freeDelivery',
            'images', 'tags', 'reviews', 'rating',
        ]

    def get_date(self, obj):
        return localtime(obj.cart.created_at).strftime('%a %b %d %Y %H:%M:%S GMT%z')

    def get_reviews(self, obj):
        if obj.product:
            return obj.product.reviews.count()
        return 0

    def get_rating(self, obj):
        if obj.product:
            reviews = obj.product.reviews.all()
            if reviews.exists():
                return round(sum(review.rate for review in reviews) / reviews.count(), 1)
        return 0


class BasketSerializer(serializers.ModelSerializer):
    products = BasketProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['products']


class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    category = serializers.IntegerField(source='product.category.id')
    title = serializers.CharField(source='product.title')
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price')
    description = serializers.CharField(source='product.description')
    freeDelivery = serializers.BooleanField(source='product.freeDelivery')
    images = ProductImageSerializer(source='product.images', many=True)
    tags = TagSerializer(source='product.tags', many=True)
    count = serializers.IntegerField()  # Поле count теперь без source
    date = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'freeDelivery',
            'images', 'tags', 'reviews', 'rating'
        ]

    def get_date(self, obj):
        return obj.order.createdAt.strftime('%a %b %d %Y %H:%M:%S GMT%z')

    def get_reviews(self, obj):
        return obj.product.reviews.count()

    def get_rating(self, obj):
        reviews = obj.product.reviews.all()
        if reviews.exists():
            return round(sum([review.rate for review in reviews]) / reviews.count(), 1)
        return 0


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    products = OrderProductSerializer(source='order_products', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType',
            'paymentType', 'totalCost', 'status', 'city', 'address', 'products'
        ]


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['src', 'alt', 'profile']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['fullName', 'phone', 'email', 'avatar']


class BannerSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'freeDelivery', 'images', 'tags', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()


class PopularProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'freeDelivery', 'images', 'tags', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()


class LimitedProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'freeDelivery', 'images', 'tags', 'reviews', 'rating')

    def get_reviews(self, obj):
        return obj.reviews.count()

