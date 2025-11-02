import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics using the INFO command and compute hit ratio.

    Returns:
        dict: {
            "keyspace_hits": int,
            "keyspace_misses": int,
            "hit_ratio": float,  # 0..1
        }
    """
    try:
        conn = get_redis_connection("default")
        try:
            info = conn.info("stats")
        except TypeError:
            info = conn.info()
    except Exception as e:
        logger.error("Failed to obtain Redis INFO: %s", e)
        return {"keyspace_hits": 0, "keyspace_misses": 0, "hit_ratio": 0}

    hits = int(info.get("keyspace_hits", 0))
    misses = int(info.get("keyspace_misses", 0))
    total_requests = hits + misses
    hit_ratio = (hits / total_requests) if total_requests > 0 else 0

    logger.info(
        "Redis cache metrics: keyspace_hits=%s keyspace_misses=%s total=%s hit_ratio=%.4f",
        hits, misses, total_requests, hit_ratio
    )

    return {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }
