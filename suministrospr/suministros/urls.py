from django.urls import path

from .views import SuministroCreate, SuministroDetail, SuministroUpdate, SuministroList

urlpatterns = [
    path("", SuministroList.as_view(), name="suministro-list"),
    path("suministros/add/", SuministroCreate.as_view(), name="suministro-add"),
    path("suministros/<int:pk>/", SuministroDetail.as_view(), name="suministro-detail"),
    path(
        "suministros/<int:pk>/edit",
        SuministroUpdate.as_view(),
        name="suministro-edit",
    ),
]
