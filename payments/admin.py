from django.contrib import admin
from .models import Payment, RegisterPayment

admin.site.register(Payment)
admin.site.register(RegisterPayment)