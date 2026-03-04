from django.contrib import admin
from django.urls import path
from .views import product_list_controller, product_detail_controller,category_list_controller,product_category_action_controller,products_by_category_controller,bulk_upload_controller

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', product_list_controller),
    path('api/v1/products/<str:product_id>/', product_detail_controller),
    path('api/v1/categories/', category_list_controller),
    path('api/v1/categories/<str:category_id>/products/', products_by_category_controller),
    path('api/v1/products/<str:product_id>/category/<str:category_id>/', product_category_action_controller),
    path('api/v1/products/<str:product_id>/category/', product_category_action_controller),
    path('api/v1/products/bulk-upload/', bulk_upload_controller),
]
