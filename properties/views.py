rom django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    queryset = get_all_properties()
    data = list(
        queryset.values(
            "id", "title", "description", "price", "location", "created_at"
        )
    )
    return JsonResponse({
        "properties": data
    })