# django_app/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import (
    create_product, get_product, list_products, 
    update_product, delete_product, 
    ValidationError, NotFoundError
)

@csrf_exempt
def product_list_controller(request):
    """Handles POST (Create) and GET (List with Pagination)"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_product = create_product(data)
            return JsonResponse({"status": "success", "data": new_product}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    elif request.method == "GET":
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            result = list_products(page=page, limit=limit)
            return JsonResponse({"status": "success", "data": result}, status=200)
        except ValueError:
            return JsonResponse({"status": "error", "message": "Pagination parameters must be integers."}, status=400)
            
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def product_detail_controller(request, product_id):
    """Handles GET (Retrieve), PUT (Update), and DELETE (Destroy) for a specific product"""
    if request.method == "GET":
        try:
            product = get_product(product_id)
            return JsonResponse({"status": "success", "data": product}, status=200)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            updated_product = update_product(product_id, data)
            return JsonResponse({"status": "success", "data": updated_product}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)

    elif request.method == "DELETE":
        try:
            result = delete_product(product_id)
            return JsonResponse({"status": "success", "data": result}, status=200)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)

    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)