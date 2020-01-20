import debug_toolbar
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", include("suministrospr.suministros.urls")),
    path("", include("pwa.urls")),
    path(r"base_layout", views.base_layout, name="base_layout"),
]
