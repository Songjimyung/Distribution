from django.contrib import admin
from .models import ShopProduct, ShopCategory


admin.site.register(ShopCategory)
admin.site.register(ShopProduct)