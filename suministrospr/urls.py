import debug_toolbar
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("", include("suministrospr.suministros.urls")),
]
