from django.db import models


class Dough(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тесто')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тесто'
        verbose_name_plural = 'Виды теста'


class ToppingGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name='Группа начинок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа начинок'
        verbose_name_plural = 'Группы начинок'


class Topping(models.Model):
    name = models.CharField(max_length=20, verbose_name='Начинка')
    price = models.FloatField(max_length=5)
    topping_group = models.ForeignKey(ToppingGroup, on_delete=models.CASCADE, related_name='toppings')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Начинка'
        verbose_name_plural = 'Начинки'
        ordering = ['name']
