from django.contrib import admin
from django.urls import path, include
from .views import TransactionViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'cashflow', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]