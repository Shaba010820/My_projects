from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from .models import (
    Transaction,
    TransactionType,
    Category,
    Status,
    Subcategory
)
class TransactionTypeSerializer(ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ('name',)

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'transaction_type')

class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('name', 'category')

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ('name',)



class TransactionSerializer(ModelSerializer):
    status = PrimaryKeyRelatedField(queryset=Status.objects.all())
    transaction_type = PrimaryKeyRelatedField(queryset=TransactionType.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = PrimaryKeyRelatedField(queryset=Subcategory.objects.all())

    class Meta:
        model = Transaction
        fields = ('id', 'created_at', 'status', 'transaction_type', 'category', 'subcategory', 'cost', 'comment')
