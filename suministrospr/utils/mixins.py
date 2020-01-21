from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language


class CacheMixin:
    cache_timeout = settings.CACHE_MIXIN_TIMEOUT
    cache_key = None

    def get_cache_key(self):
        language_code = get_language()
        return f"{self.cache_key}:{language_code}"

    def _cache_rendered_response(self, response):
        cache_key = self.get_cache_key()
        cache.set(cache_key, response, self.cache_timeout)

    def dispatch(self, *args, **kwargs):
        cache_key = self.get_cache_key()

        if cache_key:
            response = cache.get(cache_key)

            if response:
                return response

        response = super().dispatch(*args, **kwargs)

        if cache_key:
            response.add_post_render_callback(self._cache_rendered_response)

        return response
