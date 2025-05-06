from django.contrib import admin
from .models import Transaction, TransactionType, Status, Category, Subcategory
from unfold.admin import ModelAdmin

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = (
        'created_at', 'status', 'transaction_type', 'category',
        'subcategory', 'cost', 'comment'
    )
    list_filter = (
        'created_at', 'status', 'transaction_type', 'category', 'subcategory'
    )
    search_fields = ('comment',)
    autocomplete_fields = ('status', 'transaction_type', 'category', 'subcategory')
    date_hierarchy = 'created_at'



@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TransactionType)
class TransactionTypeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'transaction_type')
    list_filter = ('transaction_type',)
    search_fields = ('name',)
    autocomplete_fields = ('transaction_type',)


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ('category',)
