from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_world(request):
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
]
