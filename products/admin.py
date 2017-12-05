from django.contrib import admin
from .models import Category
from .models import Products,Cart,ProductOrder
# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(ProductOrder)