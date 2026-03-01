from django.contrib import admin
from django.urls import path
from .views import product_list_controller, product_detail_controller

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', product_list_controller),
    path('api/v1/products/<str:product_id>/', product_detail_controller),
]
