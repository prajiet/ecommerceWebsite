from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Category ( models.Model ) :
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=200)
    category_picture = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class Products ( models.Model ) :
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()
    product_discount = models.IntegerField()
    product_picture = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=50)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_favorite=models.BooleanField(default=False)
    def __str__(self):
        return self.product_brand + " - " + self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100 ,null=True)
    payment_id =models.CharField(max_length=100, null=True)

    def add_to_cart(self,product_id):
        product=Products.objects.get(pk=product_id)
        try:
            preexisting_order = ProductOrder.objects.get(product=product)
            preexisting_order.quantity +=1
            preexisting_order.save()
        except ProductOrder.DoesNotExist:
            new_order = ProductOrder.objects.create(
                product=product,
                cart=self,
                quantity=1
            )
            new_order.save()



    def remove_from_cart(self,product_id):
        product=Products.objects.get(pk=product_id)
        try:
            preexisting_order = ProductOrder.objects.get(product=product)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity = preexisting_order.quantity - 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except ProductOrder.DoesNotExist :
            pass


class ProductOrder(models.Model):
    product = models.ForeignKey(Products)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField()
    def __str__(self):
        return self.product +self.quantity






