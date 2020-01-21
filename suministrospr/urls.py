import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("suministrospr.suministros.urls")),
    path(
        "service-worker.js",
        TemplateView.as_view(
            template_name="common/service-worker.js",
            content_type="application/javascript",
        ),
        name="service-worker",
    ),
    path("offline/", TemplateView.as_view(template_name="common/offline.html",)),
]
