import debug_toolbar
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", include("suministrospr.suministros.urls")),
]
