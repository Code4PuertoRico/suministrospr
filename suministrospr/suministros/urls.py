from django.urls import path

from .views import (
    SuministroCreate,
    SuministroDetail,
    SuministroUpdate,
    SuministroList,
    SuministroByMunicipalityList,
)

urlpatterns = [
    path("", SuministroList.as_view(), name="suministro-list"),
    path("sectores/add/", SuministroCreate.as_view(), name="suministro-add"),
    path(
        "municipios/<slug:municipality>/",
        SuministroByMunicipalityList.as_view(),
        name="suministro-municipio-list",
    ),
    path(
        "sectores/<slug:slug>/", SuministroDetail.as_view(), name="suministro-detail"
    ),
    path(
        "sectores/<slug:slug>/edit",
        SuministroUpdate.as_view(),
        name="suministro-edit",
    ),
]
