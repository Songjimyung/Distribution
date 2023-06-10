from django.urls import path
from shop import views

urlpatterns = [
    # path('category/', views.CategoryAPI.as_view(), name='category_view'),
    path('products/list/<int:category_id>/',
         views.ProductViewAPI.as_view(), name='product_view'),
    path('products/<int:product_id>/',
         views.ProductDetailViewAPI.as_view(), name='product_detail_view'),
    path('categories/list', views.category_list, name='category_view')

]
