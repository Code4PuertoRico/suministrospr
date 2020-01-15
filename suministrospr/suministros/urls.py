from django.urls import path

from .views import (
    SuministroByMunicipalityList,
    SuministroCreate,
    SuministroDetail,
    SuministroList,
    SuministroUpdate,
)

urlpatterns = [
    path("", SuministroList.as_view(), name="suministro-list"),
    path("suministros/add/", SuministroCreate.as_view(), name="suministro-add"),
    path(
        "suministros/municipios/<slug:municipality>/",
        SuministroByMunicipalityList.as_view(),
        name="suministro-municipio-list",
    ),
    path(
        "suministros/<slug:slug>/", SuministroDetail.as_view(), name="suministro-detail"
    ),
    path(
        "suministros/<slug:slug>/edit",
        SuministroUpdate.as_view(),
        name="suministro-edit",
    ),
]
