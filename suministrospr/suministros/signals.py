from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save

from .models import Municipality, Suministro, Tag


def suministro_invalidate_cache(sender, instance, created=None, **kwargs):
    cache.delete_many(
        [
            "en:suministro-list",
            "es:suministro-list",
            f"en:suministro-municipio-list:{instance.municipality.slug}",
            f"es:suministro-municipio-list:{instance.municipality.slug}",
            f"en:suministro-detail:{instance.slug}",
            f"es:suministro-detail:{instance.slug}",
        ]
    )


def suministro_tags_invalidate_cache(sender, instance, action, **kwargs):
    if action in ["post_save", "post_delete"]:
        pk_set = kwargs.get("pk_set")
        cache_keys = [
            f"en:suministro-detail:{instance.slug}",
            f"es:suministro-detail:{instance.slug}",
        ]

        if pk_set:
            tag_slugs_changed = Tag.objects.filter(pk__in=pk_set).values_list(
                "slug", flat=True
            )

            for slug in tag_slugs_changed:
                cache_keys.extend(
                    [f"en:suministro-search:{slug}", f"es:suministro-search:{slug}"]
                )

        cache.delete_many(cache_keys)


def municipality_invalidate_cache(sender, instance, **kwargs):
    cache.delete_many(
        [
            "en:suministro-list",
            "es:suministro-list",
            f"en:suministro-municipio-list:{instance.slug}"
            f"es:suministro-municipio-list:{instance.slug}",
        ]
    )


def tag_invalidate_cache(sender, instance, **kwargs):
    cache.delete_many(
        [
            "en:suministro-list",
            "es:suministro-list",
            f"en:suministro-search:{instance.slug}"
            f"es:suministro-search:{instance.slug}"
            "forms:filter-tags",
        ]
    )


post_save.connect(suministro_invalidate_cache, sender=Suministro)
post_delete.connect(suministro_invalidate_cache, sender=Suministro)
m2m_changed.connect(suministro_tags_invalidate_cache, sender=Suministro.tags.through)

post_save.connect(tag_invalidate_cache, sender=Tag)
post_delete.connect(tag_invalidate_cache, sender=Tag)

post_save.connect(municipality_invalidate_cache, sender=Municipality)
post_delete.connect(municipality_invalidate_cache, sender=Municipality)
