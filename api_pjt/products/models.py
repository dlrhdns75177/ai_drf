from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = (
    ("F", "Fruit"), #앞에가 DB에 저장됨, 뒤에는 USER에게 보여짐
    ("V", "Vegetable"), 
    ("M", "Meat"),
    ("O", "Other"),
)
    name = models.CharField(max_length=30)
    price  =models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name