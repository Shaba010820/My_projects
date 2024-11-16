from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from onlineshop.views import (BannerList,
                              PopularProductList,
                              LimitedProductList,
                              CategoriesList,
                              SalesProductList,
                              TagsList,
                              CatalogView,
                              CreateUserView,
                              UserSignOut,
                              UserSignIn,
                              ProductDetailView,
                              OrderDetailView,
                              ReviewAPIView,
                              BasketAPIView,
                              ProfileView,
                              UploadAvatarView,
                              PasswordChangeView,
                              PaymentView,
                              CreateOrderView
                              )

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('banners/', BannerList.as_view(), name='banner-list'),
    path('products/popular', PopularProductList.as_view(), name='popular-product-list'),
    path('products/limited', LimitedProductList.as_view(), name='limited-product-list'),
    path('categories/', CategoriesList.as_view(), name='categories-list'),
    path('sales/', SalesProductList.as_view(), name='sale-product-list'),
    path('tags', TagsList.as_view(), name='tags-list'),
    path('catalog', CatalogView.as_view(), name='catalog-list'),
    path('sign-up', CreateUserView.as_view(), name='sign-up'),
    path('sign-out', UserSignOut.as_view(), name='sign-out'),
    path('sign-in', UserSignIn.as_view(), name='sign-in'),
    path('order/<int:id>', OrderDetailView.as_view(), name='get-one-order'),
    path('orders/', CreateOrderView.as_view(), name='create-orders'),
    path('order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders', CreateOrderView.as_view(), name='get-orders'),
    path('product/<int:id>/reviews/', ReviewAPIView.as_view(), name='product-reviews'),
    path('basket', BasketAPIView.as_view(), name='add_to_basket'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/avatar', UploadAvatarView.as_view(), name='upload-avatar'),
    path('profile/password', PasswordChangeView.as_view(), name='update-password'),
    path('payment/<int:id>', PaymentView.as_view(), name='payment'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product-detail')
]





