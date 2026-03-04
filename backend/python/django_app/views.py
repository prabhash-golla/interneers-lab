# django_app/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import (
    create_product, get_product, list_products, update_product, delete_product, ValidationError, NotFoundError,
    create_category, list_categories, list_products_by_category,
    assign_category_to_product, remove_category_from_product,
    bulk_create_products_from_csv,
)

@csrf_exempt
def category_list_controller(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category = create_category(data)
            return JsonResponse({"status": "success", "data": category}, status=201)
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    elif request.method == "GET":
        categories = list_categories()
        return JsonResponse({"status": "success", "data": categories}, status=200)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def product_category_action_controller(request, product_id, category_id=None):
    if request.method == "POST":
        try:
            result = assign_category_to_product(product_id, category_id)
            return JsonResponse({"status": "success", "data": result}, status=200)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)
    elif request.method == "DELETE":
        try:
            result = remove_category_from_product(product_id)
            return JsonResponse({"status": "success", "data": result}, status=200)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def products_by_category_controller(request, category_id):
    if request.method == "GET":
        try:
            products = list_products_by_category(category_id)
            return JsonResponse({"status": "success", "data": products}, status=200)
        except NotFoundError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def bulk_upload_controller(request):
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)
        
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"status": "error", "message": "File must be a CSV."}, status=400)
            
        result = bulk_create_products_from_csv(csv_file)
        return JsonResponse({"status": "success", "data": result}, status=201)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

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