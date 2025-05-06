from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Transaction
from .serializers import TransactionSerializer
from django_filters import rest_framework as filters


class TransactionFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status__name', lookup_expr='icontains')
    transaction_type = filters.CharFilter(field_name='transaction_type__name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    subcategory = filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')
    created_at_start = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_end = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['status', 'transaction_type', 'category', 'subcategory', 'created_at_start', 'created_at_end']


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter

