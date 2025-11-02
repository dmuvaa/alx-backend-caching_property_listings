from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    """Return a lightweight JSON payload (no serialization lib needed here)"""
    data = list(
        Property.objects.values(
            "id", "title", "description", "price", "location", "created_at"
        )
    )
    return JsonResponse(data, safe=False)
