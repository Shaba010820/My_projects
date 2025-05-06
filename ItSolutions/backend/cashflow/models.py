from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

class Transaction(models.Model):
    created_at = models.DateField('Дата создания записи', default=datetime.now)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус')
    transaction_type  = models.ForeignKey('TransactionType', on_delete=models.CASCADE, verbose_name='Тип')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, verbose_name='Подкатегория')
    cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def clean(self):
        if self.category.transaction_type != self.transaction_type :
            raise ValidationError("Выбранная категория не относится к выбранному типу.")
        if self.subcategory.category != self.category:
            raise ValidationError("Выбранная подкатегория не относится к выбранной категории.")

    def __str__(self):
        return f'{self.created_at} - {self.cost} р.'

    class Meta:
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'Движения денежных средств'


class TransactionType(models.Model):
    name = models.CharField('Название' , max_length=100)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Тип транзакции'
        verbose_name_plural = verbose_name

class Status(models.Model):
    name = models.CharField('Наименование статуса', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус транзакции'
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField('Наименование категории', max_length=100)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
                                         verbose_name='Тип транзакции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = verbose_name


class Subcategory(models.Model):
    name = models.CharField('Наименование подкатегории ', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = verbose_name