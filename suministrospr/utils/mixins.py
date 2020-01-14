from django.core.cache import cache
from django.conf import settings


class CacheMixin:
    cache_timeout = settings.CACHE_MIXIN_TIMEOUT
    cache_key = None

    def get_cache_key(self):
        return self.cache_key

    def dispatch(self, *args, **kwargs):
        cache_key = self.get_cache_key()

        if cache_key:
            response = cache.get(cache_key)

            if response:
                return response

        response = super().dispatch(*args, **kwargs)

        if cache_key:
            response.add_post_render_callback(
                lambda r: cache.set(cache_key, r, self.cache_timeout)
            )

        return response
