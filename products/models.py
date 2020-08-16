from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2,
                                validators=[MinValueValidator(0.50)])
    image = models.ImageField(upload_to='images')
    rating = models.IntegerField(default=0,
                                 validators=[MinValueValidator(0),
                                             MaxValueValidator(10)])

    def __str__(self):
        return self.product_name
