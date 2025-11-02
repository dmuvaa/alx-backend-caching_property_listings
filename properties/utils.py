from django.core.cache import cache
from .models import Property

CACHE_KEY_ALL_PROPERTIES = "all_properties"
CACHE_TTL_SECONDS = 3600

def get_all_properties():
    """Return the Property queryset, cached in Redis for 1 hour."""
    qs = cache.get(CACHE_KEY_ALL_PROPERTIES)
    if qs is None:
        qs = Property.objects.all()
        cache.set(CACHE_KEY_ALL_PROPERTIES, qs, CACHE_TTL_SECONDS)
    return qs

def getallproperties():
    return get_all_properties()