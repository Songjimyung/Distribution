from django.urls import path
from shop import views

urlpatterns = [
    path('products/list/<int:category_id>/',
         views.ProductViewAPI.as_view(), name='product_view'),
    path('products/<int:product_id>/',
         views.ProductDetailViewAPI.as_view(), name='product_detail_view'),
    path('products/list/', views.AdminProductViewAPI.as_view(),
         name='admin_product_view'),
    path('categorys/list/', views.AdminCategoryViewAPI.as_view(),
         name='admin_category_view'),
    path('category/', views.CategoryViewAPI.as_view(), name='category_view'),
    path('order/', views.OrderProductViewAPI.as_view(), name='order_view'),
    path('order/<int:order_id>/',
         views.OrderDetailViewAPI.as_view(), name='order_view')

]
