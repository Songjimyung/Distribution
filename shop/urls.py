from django.urls import path
from shop import views

urlpatterns = [
    # path('category/', views.CategoryAPI.as_view(), name='category_view'),
    path('products/<str:category_name>', views.ProductViewAPI.as_view(), name='product_view')
]
