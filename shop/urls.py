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
    path('products/order/<int:product_id>/',
         views.OrderProductViewAPI.as_view(), name='order_view'),
    path('order/list/<int:product_id>/',
         views.AdminOrderViewAPI.as_view(), name='admin_order_view'),
    path('mypage/order/', views.MypageOrderViewAPI.as_view(), name='my_order_view'),
    path('products/list/recent/', views.ProductRecentListViewAPI.as_view(),
         name='order_by_recent_view'),
    path('products/list/<int:category_id>/hits/', views.CategoryProductHitsViewAPI.as_view(),
         name='order_by_hits_view'),
    path('products/list/<int:category_id>/highprice/', views.CategoryProductHighpriceViewAPI.as_view(),
         name='order_by_highprice_view'),
    path('products/list/<int:category_id>/lowprice/', views.CategoryProductLowpriceViewAPI.as_view(),
         name='order_by_lowprice_view')
]
