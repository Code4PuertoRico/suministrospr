from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language


class CacheMixin:
    cache_timeout = settings.CACHE_MIXIN_TIMEOUT
    cache_key = None
    cache_dispatch = True

    def get_cache_key(self):
        language_code = get_language()
        return f"{language_code}:{self.cache_key}"

    def get_cache_data(self):
        cache_key = self.get_cache_key()
        return cache.get(cache_key)

    def set_cache_data(self, data):
        cache_key = self.get_cache_key()
        cache.set(cache_key, data, self.cache_timeout)

    def dispatch(self, *args, **kwargs):
        if not self.cache_dispatch:
            return super().dispatch(*args, **kwargs)

        cache_key = self.get_cache_key()

        if cache_key:
            response = self.get_cache_data()

            if response:
                return response

        response = super().dispatch(*args, **kwargs)

        if cache_key:
            response.add_post_render_callback(self.set_cache_data)

        return response
