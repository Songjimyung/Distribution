from django.contrib import admin
from .models import ShopProduct, ShopCategory, ShopOrder, ShopOrderDetail, ShopImageFile, RestockNotification


admin.site.register(ShopCategory)
admin.site.register(ShopProduct)
admin.site.register(ShopOrder)
admin.site.register(ShopOrderDetail)
admin.site.register(ShopImageFile)
admin.site.register(RestockNotification)
