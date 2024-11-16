from django.contrib.auth.models import AbstractUser, User, Group, Permission
from django.conf import settings
from django.db import models
from django.utils import timezone
import django_filters


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    deliveryType = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.TextField()
    paymentType = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    order_items = models.ManyToManyField("Product", through='OrderProduct')
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.count}"


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set')

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    freeDelivery = models.BooleanField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    description = models.TextField()
    fullDescription = models.TextField()
    specifications = models.ManyToManyField('Specification', blank=True)
    count = models.PositiveIntegerField()
    sorting_index = models.IntegerField(default=0)
    purchases_count = models.IntegerField(default=0)
    limited_edition = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    images = models.ManyToManyField('ProductImage')


    def __str__(self):
        return self.title


class Specification(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews',
                                on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.rate}'


class ProductImage(models.Model):
    src = models.ImageField(upload_to='products/')
    alt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.alt if self.alt else 'Product Image'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} в корзине {self.cart.user.username}'


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=1000000, decimal_places=2)
    salePrice = models.DecimalField(max_digits=1000000, decimal_places=2)
    dateFrom = models.DateField(default=timezone.now)
    dateTo = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255)
    images = models.ManyToManyField(ProductImage)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ForeignKey(ProductImage, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='subcategories', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def profile_preview_directory_path(instance: "Profile", filename: str) -> str:
    return "profiles/profile_{id}/preview/{filename}".format(
        id=instance.id,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    fullName = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.fullName


class Avatar(models.Model):
    profile = models.OneToOneField(Profile, related_name='avatar', on_delete=models.CASCADE)
    src = models.ImageField(blank=True, null=True)
    alt = models.CharField(max_length=50, blank=True, null=True)


def product_images_directory_path(instance: "ProfileImage", filename: str) -> str:
    return "profiles/profile_{id}/preview/{filename}".format(
        id=instance.profile.id,
        filename=filename,
    )


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    free_delivery = django_filters.BooleanFilter(field_name='free_delivery')
    available = django_filters.BooleanFilter(field_name='available')
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = ['title', 'min_price', 'max_price', 'free_delivery', 'available', 'tags']
