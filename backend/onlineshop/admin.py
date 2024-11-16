from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Product,
                     Category,
                     Tag,
                     Review,
                     Specification,
                     ProductImage,
                     Cart,
                     Order,
                     OrderProduct,
                     CartItem, Sale, CustomUser)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'username', 'is_staff', 'is_active')
    search_fields = ('name', 'username')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'freeDelivery', 'available', 'category', 'rating']
    search_fields = ['title', 'fullDescription']
    list_filter = ['available', 'freeDelivery', 'category', 'date']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("src", 'alt')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'text', 'rate', 'date')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("name", "value",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'count',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.count * obj.product.price
    total_price.short_description = 'Total Price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('createdAt', 'phone', 'email', 'deliveryType', 'city', 'address', 'fullName',
                    'paymentType', 'status')

    inlines = [OrderProductInline]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('price', 'salePrice', 'dateFrom', 'dateTo', 'title')