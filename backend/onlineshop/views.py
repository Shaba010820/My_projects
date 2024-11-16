import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (ListAPIView,
                                     get_object_or_404)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (BannerSerializer,
                          ProductSerializer,
                          CategorySerializer,
                          SaleSerializer,
                          TagSerializer,
                          CustomUserSerializer,
                          OrderSerializer,
                          ReviewSerializer,
                          BasketProductSerializer,
                          ProfileSerializer,
                          PaymentSerializer,
                          CatalogSerializer, PopularProductSerializer, LimitedProductSerializer)

from .models import (Product,
                     Cart,
                     Category,
                     Sale,
                     Tag,
                     Order,
                     OrderProduct,
                     CartItem,
                     Profile, Avatar)

from django.views.decorators.csrf import csrf_exempt

class BannerList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None


class PopularProductList(ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = PopularProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.order_by('-sorting_index', '-purchases_count')[:8]


class LimitedProductList(ListAPIView):
    model = Product
    serializer_class = LimitedProductSerializer
    queryset = Product.objects.all()
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(limited_edition=True)[:16]


class CategoriesList(ListAPIView):
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.query_params.get('sort', 'title')
        if sort in ['title', 'created_at']:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('title')

        return queryset


class ReviewAPIView(APIView):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        if isinstance(request.data, list):
            products_data = request.data
        else:
            products_data = request.data.get('products', [])

        order = Order.objects.create(user=user, status='active')

        total_price = 0

        for item in products_data:
            product = get_object_or_404(Product, id=item['id'])
            count = item.get('count', 1)
            price = product.price * count

            order_product = OrderProduct.objects.create(
                order=order,
                product=product,
                count=count,
                totalPrice=price
            )

            total_price += price

        order.totalCost = total_price
        order.save()

        return Response({"orderId": order.pk}, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    serializer_class = OrderSerializer

    def get(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, id):
        data = request.data

        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.pk = data.get('order.id', order.pk)
        order.fullName = data.get('fullName', order.fullName)
        order.email = data.get('email', order.email)
        order.phone = data.get('phone', order.phone)
        order.deliveryType = data.get('deliveryType', order.deliveryType)
        order.paymentType = data.get('paymentType', order.paymentType)
        order.city = data.get('city', order.city)
        order.address = data.get('address', order.address)
        order.status = 'accepted'
        order.save()

        return Response({'orderId': order.pk}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)



class BasketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Корзина не найдена."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()

        serializer = BasketProductSerializer(cart_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, format=None):
        product_id = request.data.get('id')
        count = request.data.get('count', 1)

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        basket_product, created = CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'count': count}
        )

        serializer = BasketProductSerializer(basket_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get('id')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=request.user)
            basket_product = CartItem.objects.get(cart=cart, product_id=product_id)
            basket_product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'error': 'Product not found in basket'}, status=status.HTTP_404_NOT_FOUND)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class CatalogView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.query_params.get('filter[name]', None)
        minPrice = self.request.query_params.get('filter[minPrice]', None)
        maxPrice = self.request.query_params.get('filter[maxPrice]', None)
        freeDelivery = self.request.query_params.get('filter[freeDelivery]', None)
        available = self.request.query_params.get('filter[available]', None)

        if name:
            queryset = queryset.filter(title__icontains=name)
        if minPrice is not None:
            queryset = queryset.filter(price__gte=minPrice)
        if maxPrice is not None:
            queryset = queryset.filter(price__lte=maxPrice)
        if freeDelivery is not None:
            queryset = queryset.filter(freeDelivery=(freeDelivery.lower() == 'true'))
        if available is not None:
            queryset = queryset.filter(available=(available.lower() == 'true'))

        tags = self.request.query_params.getlist('tags[]')
        if tags:
            queryset = queryset.filter(tags__id__in=tags).distinct()

        sort = self.request.query_params.get('sort', 'date')
        sort_type = self.request.query_params.get('sortType', 'dec')

        sort_field = 'date'
        if sort == 'rating':
            sort_field = 'rating'
        elif sort == 'price':
            sort_field = 'price'
        elif sort == 'reviews':
            sort_field = 'reviews'

        if sort_type == 'inc':
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by(f'-{sort_field}')

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'items': serializer.data, 'currentPage': 1, 'lastPage': 1}, status=status.HTTP_200_OK)


class SalesProductList(ListAPIView):
    model = Sale
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Sale.objects.filter(salePrice__gt=0).order_by('-salePrice')
        page = self.request.query_params.get('currentPage', 1)
        paginator = Paginator(queryset, 20)
        return paginator.get_page(page)


class TagsList(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class CreateUserView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        if isinstance(data, dict) and 'username' not in data:
            data_string = list(data.keys())[0]
            data = json.loads(data_string)

        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(data['password'])
            user = authenticate(request, username=user.name, password=data['password'])

            if user is not None:
                login(request, user)
                return Response({'detail': 'User created and logged in successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'User created but failed to log in.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignOut(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class UserSignIn(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get('username'):
            data = request.data
        else:
            data_string = list(request.data.keys())[0]
            data = json.loads(data_string)

        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'avatar' not in request.FILES:
            return JsonResponse({'error': 'Avatar file is required.'}, status=400)

        avatar_file = request.FILES['avatar']

        user_profile, created = Profile.objects.get_or_create(user=request.user)

        avatar_instance, created = Avatar.objects.get_or_create(profile=user_profile)
        avatar_instance.src = avatar_file
        avatar_instance.save()

        return JsonResponse({'message': 'Avatar updated successfully.'}, status=200)


class PasswordChangeView(APIView):
    def post(self, request):
        user = request.user
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({'message': 'Password updated successfully'})


class PaymentView(APIView):
    def post(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order.status = 'paid'
            order.save()

            for product in order.order_items.all():
                product.purchases_count += product.count
                product.save()

            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
