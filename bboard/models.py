from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

def validate_even(val):
    if val % 2 == 0:
        return ValidationError('Число %(value)s нечётное', code='add',
    params={'value': val})

class MinMaxValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    #def __call__(self, val):
        #if val < self.min_value or val > self.max_value:
            #raise ValidationError(%(min)%),
        #code='out'

class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name="Название",
    )

    def __str__(self):
        return f'{self.name}'

    #def get_absolute_url(self):
    #    return f"{self.pk}/"


    #def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)

    #def delete(self, *args, **kwargs):
    #    super().delete(*args, **kwargs)
    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

class Bb(models.Model):
    #KINDS = (
    #    ('b', 'Куплю'),
    #    ('s', 'Продам'),
    #    ('c', 'Обмен'),
    #)

    KINDS = (
        ('Купля-продажа',(
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        ))
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Ведите 4 и болие символа'},
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    #price = models.FloatField(
    #    null=True,
    #    blank=True,
    #    verbose_name='Цена')

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Цена',
        validators=[validate_even]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опобликовано',
    )

    def titel_and_price(self):
        if self.price:
            return f'{self.title} {self.price:.2f}'
        return self.title

    def __str__(self):
        return f'{self.title}({self.price} тнг)'

    class Meta:
        ordering = ['-published','title']
        #order_with_respect_to = 'rubric'

        unique_together = ('title','published')
        verbose_name = 'Обявление'
        verbose_name_plural = 'Объявления'

    #titel_and_price.

    def clean(self):
        errors = {}
        if not self.content:
            errors['price'] = ValidationError('')