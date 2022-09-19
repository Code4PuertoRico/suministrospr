from django.urls import path

from .views import (
    SuministroByMunicipalityList,
    SuministroCreate,
    SuministroDetail,
    SuministroList,
    SuministroSearch,
    SuministroServiceWorker,
    SuministroUpdate,
)

urlpatterns = [
    path("", SuministroList.as_view(), name="suministro-list"),
    path("buscar/", SuministroSearch.as_view(), name="suministro-search"),
    path("sectores/add/", SuministroCreate.as_view(), name="suministro-add"),
    path(
        "municipios/<slug:municipality>/",
        SuministroByMunicipalityList.as_view(),
        name="suministro-municipio-list",
    ),
    path("sectores/<slug:slug>/", SuministroDetail.as_view(), name="suministro-detail"),
    path(
        "sectores/<slug:slug>/edit",
        SuministroUpdate.as_view(),
        name="suministro-edit",
    ),
    path(
        "service-worker.js",
        SuministroServiceWorker.as_view(),
        name="service-worker",
    ),
]
